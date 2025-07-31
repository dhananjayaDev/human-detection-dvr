import telegram
import asyncio
import logging
from typing import Optional, List
from datetime import datetime, timedelta
import cv2
import numpy as np
from io import BytesIO

class TelegramAlert:
    def __init__(self, bot_token: str, chat_id: str, cooldown_seconds: int = 30):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = None
        self.bot = None
        self.logger = logging.getLogger(__name__)
        
    def initialize(self) -> bool:
        """Initialize Telegram bot"""
        try:
            self.bot = telegram.Bot(token=self.bot_token)
            # Test connection
            asyncio.run(self.bot.get_me())
            self.logger.info("Telegram bot initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Telegram bot: {e}")
            return False
    
    def can_send_alert(self) -> bool:
        """Check if enough time has passed since last alert"""
        if self.last_alert_time is None:
            return True
        
        time_since_last = datetime.now() - self.last_alert_time
        return time_since_last.total_seconds() >= self.cooldown_seconds
    
    async def send_alert(self, frame: np.ndarray, detection_count: int) -> bool:
        """Send alert with frame image"""
        if not self.can_send_alert():
            self.logger.info("Alert skipped due to cooldown")
            return False
        
        try:
            # Prepare message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"🚨 HUMAN DETECTED!\n\n"
            message += f"📅 Time: {timestamp}\n"
            message += f"👥 Detections: {detection_count}\n"
            message += f"📍 Location: Camera Feed"
            
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            image_bytes = BytesIO(buffer.tobytes())
            
            # Send message with image
            await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=image_bytes,
                caption=message
            )
            
            self.last_alert_time = datetime.now()
            self.logger.info(f"Alert sent successfully to {self.chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram alert: {e}")
            return False
    
    def send_alert_sync(self, frame: np.ndarray, detection_count: int) -> bool:
        """Synchronous wrapper for send_alert"""
        try:
            return asyncio.run(self.send_alert(frame, detection_count))
        except Exception as e:
            self.logger.error(f"Error in sync alert: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test bot connection"""
        try:
            asyncio.run(self.bot.get_me())
            self.logger.info("Telegram bot connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"Telegram bot connection test failed: {e}")
            return False 