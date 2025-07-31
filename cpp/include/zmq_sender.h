#ifndef ZMQ_SENDER_H
#define ZMQ_SENDER_H

#include <zmq.hpp>
#include <opencv2/opencv.hpp>
#include <string>

class ZMQSender {
public:
    ZMQSender(const std::string& address = "tcp://*:5555");
    ~ZMQSender();
    
    bool initialize();
    bool send_frame(const cv::Mat& frame);
    void close();
    
    void set_address(const std::string& address);
    bool is_connected() const;
    
private:
    zmq::context_t context_;
    std::unique_ptr<zmq::socket_t> socket_;
    std::string address_;
    bool connected_;
    
    bool serialize_frame(const cv::Mat& frame, std::vector<uchar>& buffer);
};

#endif // ZMQ_SENDER_H 