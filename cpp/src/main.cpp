#include "video_capture.h"
#include <iostream>
#include <signal.h>
#include <json/json.h>

static bool running = true;

void signal_handler(int signal) {
    std::cout << "\nReceived signal " << signal << ", shutting down..." << std::endl;
    running = false;
}

bool load_config(VideoCapture& capture, const std::string& config_file) {
    try {
        std::ifstream file(config_file);
        if (!file.is_open()) {
            std::cerr << "Could not open config file: " << config_file << std::endl;
            return false;
        }
        
        Json::Value root;
        Json::CharReaderBuilder builder;
        std::string errors;
        
        if (!Json::parseFromStream(builder, file, &root, &errors)) {
            std::cerr << "JSON parsing error: " << errors << std::endl;
            return false;
        }
        
        // Load camera settings
        if (root.isMember("camera_index")) {
            capture.set_camera_index(root["camera_index"].asInt());
        }
        
        if (root.isMember("frame_width") && root.isMember("frame_height")) {
            capture.set_resolution(root["frame_width"].asInt(), root["frame_height"].asInt());
        }
        
        if (root.isMember("fps")) {
            capture.set_fps(root["fps"].asInt());
        }
        
        if (root.isMember("zmq_port")) {
            capture.set_zmq_port(root["zmq_port"].asInt());
        }
        
        std::cout << "Configuration loaded from " << config_file << std::endl;
        return true;
        
    } catch (const std::exception& e) {
        std::cerr << "Error loading config: " << e.what() << std::endl;
        return false;
    }
}

int main(int argc, char* argv[]) {
    std::cout << "=== Hybrid AI-Powered DVR System ===" << std::endl;
    std::cout << "C++ Video Capture Component" << std::endl;
    std::cout << "=====================================" << std::endl;
    
    // Set up signal handling
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    // Default configuration
    VideoCapture capture(0, 640, 480, 30);
    
    // Load configuration if provided
    std::string config_file = "../config/camera_config.json";
    if (argc > 1) {
        config_file = argv[1];
    }
    
    if (!load_config(capture, config_file)) {
        std::cout << "Using default configuration" << std::endl;
    }
    
    // Initialize video capture
    if (!capture.initialize()) {
        std::cerr << "Failed to initialize video capture" << std::endl;
        return 1;
    }
    
    // Run the capture loop
    std::cout << "Press Ctrl+C to stop" << std::endl;
    capture.run();
    
    std::cout << "Video capture component stopped" << std::endl;
    return 0;
} 