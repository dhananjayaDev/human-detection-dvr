import zmq
import cv2
import numpy as np
from typing import Optional, Tuple
import logging

class ZMQReceiver:
    def __init__(self, address: str = "tcp://localhost:5555"):
        self.address = address
        self.context = zmq.Context()
        self.socket = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
        
    def initialize(self) -> bool:
        """Initialize ZMQ subscriber connection"""
        try:
            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect(self.address)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
            self.connected = True
            self.logger.info(f"ZMQ Receiver connected to {self.address}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize ZMQ receiver: {e}")
            return False
    
    def receive_frame(self, timeout_ms: int = 1000) -> Optional[np.ndarray]:
        """Receive a frame from ZMQ with timeout"""
        if not self.connected or not self.socket:
            return None
            
        try:
            # Set timeout
            self.socket.setsockopt(zmq.RCVTIMEO, timeout_ms)
            
            # Receive frame data
            frame_data = self.socket.recv()
            
            # Decode frame
            frame_array = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            return frame
            
        except zmq.Again:
            # Timeout occurred
            return None
        except Exception as e:
            self.logger.error(f"Error receiving frame: {e}")
            return None
    
    def close(self):
        """Close ZMQ connection"""
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()
        self.connected = False
        self.logger.info("ZMQ Receiver closed")
    
    def is_connected(self) -> bool:
        return self.connected 