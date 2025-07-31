# Human Detection DVR

![Banner Image](https://github.com/dhananjayaDev/human-detection-dvr/blob/master/HDDDVR%20Bannner.png)

## Overview
This repository contains the source code and documentation for a Human Detection DVR (Digital Video Recorder) system. The project aims to implement real-time human detection using computer vision techniques, integrated with a DVR system for surveillance and monitoring purposes.

## Features
- **Real-Time Human Detection**: Utilizes advanced computer vision algorithms to detect humans in video feeds.
- **DVR Integration**: Seamlessly records and stores video footage with human detection events.
- **Customizable Alerts**: Configurable notifications for detected human activities.
- **User-Friendly Interface**: Simple and intuitive UI for managing recordings and settings.

## Requirements
- Python 3.8+
- OpenCV
- TensorFlow or PyTorch (depending on the model used)
- FFmpeg for video processing
- A compatible DVR hardware or software setup

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dhananjayaDev/human-detection-dvr.git
   cd human-detection-dvr
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the DVR settings in `config.yaml` (create this file based on `config.example.yaml`).
4. Run the application:
   ```bash
   python main.py
   ```

## Usage
- Launch the application using the command above.
- Access the web interface at `http://localhost:5000` (or the configured port).
- Configure detection parameters and DVR settings through the interface.
- Monitor real-time detection and review recorded footage.

## Project Structure
```
human-detection-dvr/
├── config.example.yaml      # Example configuration file
├── main.py                 # Entry point for the application
├── requirements.txt        # Python dependencies
├── src/                    # Source code
│   ├── detection/          # Human detection logic
│   ├── dvr/                # DVR integration module
│   └── ui/                 # User interface components
└── docs/                   # Documentation
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please open an issue or contact the maintainer at [dhananjaya.dev@email.com](mailto:dhananjaya.dev@email.com).
