#!/usr/bin/env python3
"""
System runner script for the Hybrid AI-Powered DVR System
"""

import subprocess
import sys
import os
import signal
import time
import logging
from pathlib import Path

class SystemRunner:
    def __init__(self):
        self.cpp_process = None
        self.python_process = None
        self.logger = logging.getLogger(__name__)
        
    def start_cpp_component(self):
        """Start the C++ video capture component"""
        try:
            cpp_executable = Path("../cpp/Debug/video_capture.exe")
            if not cpp_executable.exists():
                self.logger.error(f"C++ executable not found: {cpp_executable}")
                return False
                
            self.cpp_process = subprocess.Popen(
                [str(cpp_executable)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.logger.info("C++ video capture component started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start C++ component: {e}")
            return False
    
    def start_python_component(self):
        """Start the Python detection component"""
        try:
            python_script = Path("../python/detection/human_detector.py")
            if not python_script.exists():
                self.logger.error(f"Python script not found: {python_script}")
                return False
                
            self.python_process = subprocess.Popen(
                [sys.executable, str(python_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.logger.info("Python detection component started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Python component: {e}")
            return False
    
    def stop_components(self):
        """Stop all running components"""
        if self.cpp_process:
            self.cpp_process.terminate()
            self.logger.info("C++ component stopped")
            
        if self.python_process:
            self.python_process.terminate()
            self.logger.info("Python component stopped")
    
    def run(self):
        """Run the complete system"""
        print("=== Hybrid AI-Powered DVR System ===")
        print("Starting system components...")
        print("=====================================")
        
        # Start C++ component
        if not self.start_cpp_component():
            print("Failed to start C++ component")
            return
        
        # Wait a moment for C++ component to initialize
        time.sleep(2)
        
        # Start Python component
        if not self.start_python_component():
            print("Failed to start Python component")
            self.stop_components()
            return
        
        print("System started successfully!")
        print("Press Ctrl+C to stop all components")
        
        try:
            # Keep running until interrupted
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if self.cpp_process and self.cpp_process.poll() is not None:
                    print("C++ component stopped unexpectedly")
                    break
                    
                if self.python_process and self.python_process.poll() is not None:
                    print("Python component stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            print("\nShutting down system...")
        finally:
            if self.cpp_process:
                out, err = self.cpp_process.communicate()
                print("C++ stdout:", out.decode())
                print("C++ stderr:", err.decode())
            if self.python_process:
                out, err = self.python_process.communicate()
                print("Python stdout:", out.decode())
                print("Python stderr:", err.decode())
            self.stop_components()
            print("System stopped")

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    runner = SystemRunner()
    runner.run()

if __name__ == "__main__":
    main()