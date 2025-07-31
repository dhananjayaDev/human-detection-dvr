# Human Detection DVR

![Banner Image](https://github.com/dhananjayaDev/human-detection-dvr/blob/master/HDDDVR%20Bannner.png)

## Overview
This repository contains the source code for a Human Detection DVR (Digital Video Recorder) system. The project implements real-time human detection using computer vision techniques, integrated with a DVR system for surveillance and monitoring purposes. It leverages a decoupled architecture with C++ for video capture and Python for human detection and alerting, communicating via ZeroMQ.

## Features
- **Real-Time Human Detection**: Utilizes YOLOv5, a state-of-the-art object detection model, to detect humans in live video feeds.
- **Modular Architecture**: Separates video capture (C++) from human detection and alerting (Python) using ZeroMQ for efficient inter-process communication.
- **Configurable Alerts**: Sends real-time alerts with snapshots to Telegram upon human detection, with a customizable cooldown period.
- **Flexible Video Input**: Captures video from various sources via OpenCV, allowing for different camera setups.
- **Customizable Detection Parameters**: Allows configuration of detection confidence thresholds and Telegram alert settings via JSON files.

## Requirements
- Python 3.8+
- OpenCV
- PyTorch (for YOLOv5)
- ZeroMQ libraries (for inter-process communication)
- Telegram Bot API (for alerts)
- FFmpeg (for video processing, if applicable for DVR hardware/software)
- A compatible camera or video source

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dhananjayaDev/human-detection-dvr.git
   cd human-detection-dvr
   ```
2. Install Python dependencies:
   ```bash
   pip install -r python/requirements.txt
   ```
3. Build the C++ component (requires CMake and a C++ compiler, e.g., g++ or MSVC):
   ```bash
   # Example for Linux
   cd cpp
   mkdir build
   cd build
   cmake ..
   make
   # For Windows, use Visual Studio to open HumanDetectionDVR.sln and build
   ```
4. Configure the system:
   - Edit `config/camera_config.json` for camera settings (index, resolution, FPS).
   - Edit `config/detection_config.json` for detection parameters (confidence threshold, Telegram bot token, chat ID, alert cooldown).

## Usage
1. Start the C++ video capture component (from the `cpp/build` directory after building):
   ```bash
   ./video_capture_executable
   ```
   (The exact executable name might vary based on your build system, e.g., `HumanDetectionDVR` on Windows)
2. Start the Python human detection component (from the root `human-detection-dvr` directory):
   ```bash
   python python/detection/human_detector.py
   ```
3. Monitor real-time human detection in the OpenCV display window (if enabled) and receive Telegram alerts.

## Project Structure
```
human-detection-dvr/
├── config/                 # Configuration files (JSON)
│   ├── camera_config.json  # Camera settings
│   └── detection_config.json # Detection and alert settings
├── cpp/                    # C++ Video Capture Component
│   ├── include/            # Header files
│   ├── src/                # Source files (video_capture, zmq_sender)
│   └── CMakeLists.txt      # CMake build script
├── python/                 # Python Human Detection Component
│   ├── detection/          # Core detection logic
│   │   ├── human_detector.py # Main detection script (YOLOv5, ZMQ receiver, Telegram alert)
│   │   ├── zmq_receiver.py   # ZeroMQ frame receiver
│   │   └── telegram_alert.py # Telegram alert sender
│   └── requirements.txt    # Python dependencies
├── scripts/                # Utility scripts (e.g., run_system.py, yolov5su.pt)
├── vcpkg/                  # C++ package manager (if used for dependencies)
├── HDDDVR Bannner.png      # Banner image for README
└── README.md               # This README file
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/dhananjayaDev/human-detection-dvr?tab=MIT-1-ov-file) file for details.

## Contact
For questions or support, please open an issue or contact the maintainer at [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/dhananjayadissanayake/).


