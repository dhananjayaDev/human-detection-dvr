#include "video_capture.h"
#include <iostream>
#include <chrono>
#include <thread>

VideoCapture::VideoCapture(int camera_index, int width, int height, int fps)
    : camera_index_(camera_index), frame_width_(width), frame_height_(height), 
      fps_(fps), zmq_port_(5555), running_(false) {
    zmq_sender_ = std::make_unique<ZMQSender>("tcp://*:" + std::to_string(zmq_port_));
}

VideoCapture::~VideoCapture() {
    stop();
}

bool VideoCapture::initialize() {
    // Initialize camera
    cap_.open(camera_index_);
    if (!cap_.isOpened()) {
        log_error("Failed to open camera at index " + std::to_string(camera_index_));
        return false;
    }
    
    // Set camera properties
    cap_.set(cv::CAP_PROP_FRAME_WIDTH, frame_width_);
    cap_.set(cv::CAP_PROP_FRAME_HEIGHT, frame_height_);
    cap_.set(cv::CAP_PROP_FPS, fps_);
    
    // Initialize ZMQ sender
    if (!zmq_sender_->initialize()) {
        log_error("Failed to initialize ZMQ sender");
        return false;
    }
    
    std::cout << "Video capture initialized successfully" << std::endl;
    std::cout << "Camera: " << camera_index_ << std::endl;
    std::cout << "Resolution: " << frame_width_ << "x" << frame_height_ << std::endl;
    std::cout << "FPS: " << fps_ << std::endl;
    std::cout << "ZMQ Port: " << zmq_port_ << std::endl;
    
    return true;
}

void VideoCapture::run() {
    if (!cap_.isOpened()) {
        log_error("Camera not initialized");
        return;
    }
    
    running_ = true;
    std::cout << "Starting video capture..." << std::endl;
    
    auto frame_interval = std::chrono::microseconds(1000000 / fps_);
    
    while (running_) {
        auto start_time = std::chrono::high_resolution_clock::now();
        
        if (!capture_and_send_frame()) {
            log_error("Failed to capture and send frame");
            break;
        }
        
        // Maintain frame rate
        auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
        if (elapsed < frame_interval) {
            std::this_thread::sleep_for(frame_interval - elapsed);
        }
    }
    
    std::cout << "Video capture stopped" << std::endl;
}

void VideoCapture::stop() {
    running_ = false;
}

bool VideoCapture::is_running() const {
    return running_;
}

bool VideoCapture::capture_and_send_frame() {
    cv::Mat frame;
    if (!cap_.read(frame)) {
        return false;
    }
    
    // Resize frame if needed
    if (frame.cols != frame_width_ || frame.rows != frame_height_) {
        cv::resize(frame, frame, cv::Size(frame_width_, frame_height_));
    }
    
    // Send frame via ZMQ
    return zmq_sender_->send_frame(frame);
}

void VideoCapture::set_camera_index(int index) {
    camera_index_ = index;
}

void VideoCapture::set_resolution(int width, int height) {
    frame_width_ = width;
    frame_height_ = height;
}

void VideoCapture::set_fps(int fps) {
    fps_ = fps;
}

void VideoCapture::set_zmq_port(int port) {
    zmq_port_ = port;
    zmq_sender_ = std::make_unique<ZMQSender>("tcp://*:" + std::to_string(zmq_port_));
}

void VideoCapture::log_error(const std::string& message) {
    std::cerr << "[ERROR] " << message << std::endl;
} 