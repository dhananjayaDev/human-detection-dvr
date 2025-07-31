#ifndef VIDEO_CAPTURE_H
#define VIDEO_CAPTURE_H

#include <opencv2/opencv.hpp>
#include <string>
#include <memory>
#include "zmq_sender.h"

class VideoCapture {
public:
    VideoCapture(int camera_index = 0, int width = 640, int height = 480, int fps = 30);
    ~VideoCapture();
    
    bool initialize();
    void run();
    void stop();
    bool is_running() const;
    
    // Configuration
    void set_camera_index(int index);
    void set_resolution(int width, int height);
    void set_fps(int fps);
    void set_zmq_port(int port);
    
private:
    cv::VideoCapture cap_;
    std::unique_ptr<ZMQSender> zmq_sender_;
    
    int camera_index_;
    int frame_width_;
    int frame_height_;
    int fps_;
    int zmq_port_;
    bool running_;
    
    bool capture_and_send_frame();
    void log_error(const std::string& message);
};

#endif // VIDEO_CAPTURE_H 