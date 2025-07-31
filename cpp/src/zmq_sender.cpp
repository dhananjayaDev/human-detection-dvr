#include "zmq_sender.h"
#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include <json/json.h>

ZMQSender::ZMQSender(const std::string& address)
    : context_(1), address_(address), connected_(false) {
}

ZMQSender::~ZMQSender() {
    close();
}

bool ZMQSender::initialize() {
    try {
        socket_ = std::make_unique<zmq::socket_t>(context_, ZMQ_PUB);
        socket_->bind(address_);
        connected_ = true;
        std::cout << "ZMQ Sender initialized on " << address_ << std::endl;
        return true;
    } catch (const zmq::error_t& e) {
        std::cerr << "ZMQ initialization error: " << e.what() << std::endl;
        return false;
    }
}

bool ZMQSender::send_frame(const cv::Mat& frame) {
    if (!connected_ || !socket_) {
        return false;
    }
    
    try {
        std::vector<uchar> buffer;
        if (!serialize_frame(frame, buffer)) {
            return false;
        }
        
        zmq::message_t message(buffer.size());
        memcpy(message.data(), buffer.data(), buffer.size());
        
        return socket_->send(message, zmq::send_flags::none).has_value();
    } catch (const zmq::error_t& e) {
        std::cerr << "ZMQ send error: " << e.what() << std::endl;
        return false;
    }
}

void ZMQSender::close() {
    if (socket_) {
        socket_->close();
        socket_.reset();
    }
    connected_ = false;
}

void ZMQSender::set_address(const std::string& address) {
    address_ = address;
}

bool ZMQSender::is_connected() const {
    return connected_;
}

bool ZMQSender::serialize_frame(const cv::Mat& frame, std::vector<uchar>& buffer) {
    try {
        // Encode frame as JPEG for efficient transmission
        std::vector<int> compression_params;
        compression_params.push_back(cv::IMWRITE_JPEG_QUALITY);
        compression_params.push_back(85); // Good quality, reasonable size
        
        return cv::imencode(".jpg", frame, buffer, compression_params);
    } catch (const cv::Exception& e) {
        std::cerr << "Frame serialization error: " << e.what() << std::endl;
        return false;
    }
}

