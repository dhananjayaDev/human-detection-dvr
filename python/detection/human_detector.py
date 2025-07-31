import cv2
import numpy as np
import torch
import logging
import time
from typing import List, Tuple, Optional
from ultralytics import YOLO
from zmq_receiver import ZMQReceiver
from telegram_alert import TelegramAlert
import json
import os

class HumanDetector:
    def __init__(self, config_file: str = "../config/detection_config.json"):
        self.config_file = config_file
        self.model = None
        self.zmq_receiver = None
        self.telegram_alert = None
        self.confidence_threshold = 0.5
        self.running = False
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.load_config()
        
    def load_config(self):
        """Load detection configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            self.confidence_threshold = config.get('confidence_threshold', 0.5)
            telegram_token = config.get('telegram_bot_token', '')
            telegram_chat_id = config.get('telegram_chat_id', '')
            alert_cooldown = config.get('alert_cooldown', 30)
            
            # Initialize Telegram alert if configured
            if telegram_token and telegram_chat_id:
                self.telegram_alert = TelegramAlert(
                    telegram_token, telegram_chat_id, alert_cooldown
                )
                
            self.logger.info("Configuration loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
    
    def initialize(self) -> bool:
        """Initialize the detection system"""
        try:
            # Load YOLOv5 model
            self.model = YOLO('yolov5s.pt')
            self.logger.info("YOLOv5 model loaded successfully")
            
            # Initialize ZMQ receiver
            self.zmq_receiver = ZMQReceiver()
            if not self.zmq_receiver.initialize():
                self.logger.error("Failed to initialize ZMQ receiver")
                return False
            
            # Initialize Telegram alert if configured
            if self.telegram_alert:
                if not self.telegram_alert.initialize():
                    self.logger.warning("Failed to initialize Telegram alert")
                    self.telegram_alert = None
            
            self.logger.info("Human detection system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize detection system: {e}")
            return False
    
    def detect_humans(self, frame: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """Detect humans in frame using YOLOv5"""
        try:
            # Run inference
            results = self.model(frame, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates and confidence
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        
                        # Only detect humans (class 0 in COCO dataset)
                        if class_id == 0 and confidence >= self.confidence_threshold:
                            detections.append((int(x1), int(y1), int(x2), int(y2), confidence))
            
            return detections
            
        except Exception as e:
            self.logger.error(f"Error in human detection: {e}")
            return []
    
    def draw_detections(self, frame: np.ndarray, detections: List[Tuple[int, int, int, int, float]]) -> np.ndarray:
        """Draw detection boxes on frame"""
        for x1, y1, x2, y2, confidence in detections:
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw confidence label
            label = f"Human: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame
    
    def run(self):
        """Main detection loop"""
        if not self.initialize():
            return
        
        self.running = True
        self.logger.info("Starting human detection...")
        
        frame_count = 0
        start_time = time.time()
        
        while self.running:
            try:
                # Receive frame from ZMQ
                frame = self.zmq_receiver.receive_frame(timeout_ms=1000)
                if frame is None:
                    continue
                
                # Detect humans
                detections = self.detect_humans(frame)
                
                # Draw detections
                frame_with_boxes = self.draw_detections(frame.copy(), detections)
                
                # Send alert if humans detected
                if detections and self.telegram_alert:
                    self.telegram_alert.send_alert_sync(frame_with_boxes, len(detections))
                
                # Display frame (optional)
                cv2.imshow('Human Detection', frame_with_boxes)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # Calculate FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed
                    self.logger.info(f"FPS: {fps:.2f}, Detections: {len(detections)}")
                
            except KeyboardInterrupt:
                self.logger.info("Detection stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in detection loop: {e}")
                continue
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.zmq_receiver:
            self.zmq_receiver.close()
        cv2.destroyAllWindows()
        self.logger.info("Detection system stopped")

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=== Human Detection System ===")
    print("Python AI Detection Component")
    print("==============================")
    
    # Create and run detector
    detector = HumanDetector()
    detector.run()

if __name__ == "__main__":
    main() 