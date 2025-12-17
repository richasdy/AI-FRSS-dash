import cv2
import time
import threading
import asyncio
import logging
import os
import imagehash
from PIL import Image
from typing import Dict, List, Any
import httpx
from datetime import datetime
from app.services.models_service import yolo_service
import numpy as np
import io

# Configure logging
logger = logging.getLogger(__name__)

class PeopleDetectionService:
    def __init__(self):
        self.is_running = False
        self.camera_url = os.getenv("CCTV_STREAM_URL", "http://cctv-stream-url/stream") # Configure via env
        self.backend_url = os.getenv("NODE_BACKEND_URL", "http://localhost:3000/api/detections") # Configure via env
        self.fps = 1.0 # Process 1 frame per second
        self.confidence_threshold = 0.5
        self.hash_threshold = 5 # Hamming distance threshold
        self.recent_hashes = [] # List of (hash, timestamp)
        self.hash_cleanup_time = 300 # Keep hashes for 5 minutes
        self.thread = None
        self.loop = None

    def start(self):
        if self.is_running:
            logger.warning("People detection service is already running")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("People detection service started")

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        logger.info("People detection service stopped")

    def _run_loop(self):
        # Create a new event loop for this thread to run async tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.loop = loop
        
        cap = cv2.VideoCapture(self.camera_url)
        
        # Fallback for testing if camera not available
        if not cap.isOpened():
             logger.warning(f"Could not open camera stream: {self.camera_url}")
             # In a real scenario, we might want to retry or exit
             # For now, let's just exit the loop if we can't connect
             self.is_running = False
             return

        last_process_time = 0
        frame_interval = 1.0 / self.fps

        while self.is_running:
            current_time = time.time()
            
            # Clean up old hashes
            self._cleanup_hashes()
            
            ret, frame = cap.read()
            if not ret:
                logger.warning("Failed to read frame from stream")
                time.sleep(1) # Wait before retrying
                # Reconnect logic could go here
                cap.release()
                cap = cv2.VideoCapture(self.camera_url)
                continue

            if current_time - last_process_time >= frame_interval:
                last_process_time = current_time
                
                # Run detection in the async loop
                try:
                    loop.run_until_complete(self._process_frame(frame))
                except Exception as e:
                    logger.error(f"Error processing frame: {e}")

            # Sleep slightly to reduce CPU usage
            time.sleep(0.01)

        cap.release()
        loop.close()

    async def _process_frame(self, frame):
        # Convert frame to format expected by YOLO service (base64 or PIL)
        # YOLO service expects base64 string in detect_objects_optimized
        
        # Convert OpenCV BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        # Convert to base64
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Run detection
        # We use 'people' model
        result = await yolo_service.detect_objects_optimized(
            model_type="people",
            image_data=img_str,
            confidence=self.confidence_threshold
        )
        
        if not result["success"]:
            return

        detections = result["detections"]
        timestamp = datetime.now()

        for detection in detections:
            # Extract bounding box
            bbox = detection["bbox"] # [x1, y1, x2, y2]
            x1, y1, x2, y2 = map(int, bbox)
            
            # Ensure coordinates are within image bounds
            h, w, _ = frame.shape
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            if x2 <= x1 or y2 <= y1:
                continue
                
            # Crop person
            person_crop = pil_image.crop((x1, y1, x2, y2))
            
            # Calculate pHash
            current_hash = imagehash.phash(person_crop)
            
            # Check for duplicates
            if self._is_duplicate(current_hash):
                continue
            
            # New person detected
            logger.info(f"New person detected! Hash: {current_hash}")
            self.recent_hashes.append((current_hash, time.time()))
            
            # Send to backend
            await self._send_to_backend(person_crop, detection, timestamp)

    def _is_duplicate(self, current_hash):
        for stored_hash, _ in self.recent_hashes:
            if current_hash - stored_hash <= self.hash_threshold:
                return True
        return False

    def _cleanup_hashes(self):
        current_time = time.time()
        self.recent_hashes = [
            (h, t) for (h, t) in self.recent_hashes 
            if current_time - t < self.hash_cleanup_time
        ]

    async def _send_to_backend(self, image, detection, timestamp):
        try:
            # Save image to buffer
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            
            # Prepare data
            files = {'image': ('person.jpg', img_byte_arr, 'image/jpeg')}
            data = {
                'timestamp': timestamp.isoformat(),
                'cameraId': 'camera_1', # TODO: make dynamic
                'confidence': str(detection['confidence']),
                'box': str(detection['bbox']),
                'phash': str(imagehash.phash(image))
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.backend_url, data=data, files=files)
                
            if response.status_code == 201:
                logger.info("Successfully sent detection to backend")
            else:
                logger.error(f"Failed to send detection: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error sending to backend: {e}")

import base64
# Global instance
people_detection_service = PeopleDetectionService()
