import cv2
import threading
import time
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class StreamCapture:
    def __init__(self):
        self.url = settings.VIDEO_SOURCE
        self.cap = None
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        self.current_frame = None
        self.last_frame_time = 0
        self.reconnect_delay = 5  # Seconds
        self.frame_count = 0

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        logger.info("Stream capture started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        logger.info("Stream capture stopped.")

    def _capture_loop(self):
        while self.running:
            try:
                if self.cap is None or not self.cap.isOpened():
                    logger.info(f"Connecting to stream: {self.url}")
                    self.cap = cv2.VideoCapture(self.url)
                    if not self.cap.isOpened():
                        logger.error("Failed to open stream. Retrying...")
                        time.sleep(self.reconnect_delay)
                        continue
                    logger.info("Stream opened successfully.")

                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Failed to read frame. Reconnecting...")
                    self.cap.release()
                    self.cap = None
                    time.sleep(1) 
                    continue

                with self.lock:
                    self.current_frame = frame
                    self.last_frame_time = time.time()
                    self.frame_count += 1
                
                if self.frame_count % 100 == 0:
                    logger.info(f"Stream capture active. Total frames: {self.frame_count}")
                
                # Sleep a bit to avoid CPU spin if read() returns instantly (it won't on this stream)
                time.sleep(0.01)

            except Exception as e:
                logger.error(f"Error in capture loop: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
                time.sleep(self.reconnect_delay)

    def get_frame(self):
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
            return None
