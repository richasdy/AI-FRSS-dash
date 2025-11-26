import torch
import numpy as np
import cv2
from ultralytics import YOLO
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PeopleDetector:
    def __init__(self):
        self.device = self._get_device()
        self.model = self._load_model()
        
    def _get_device(self):
        """
        Selects the appropriate device: MPS (Apple Silicon), CUDA (NVIDIA), or CPU.
        """
        if torch.backends.mps.is_available():
            logger.info("Using Apple Silicon MPS acceleration.")
            return "mps"
        elif torch.cuda.is_available():
            logger.info("Using CUDA acceleration.")
            return "cuda"
        else:
            logger.info("Using CPU fallback.")
            return "cpu"

    def _load_model(self):
        try:
            logger.info(f"Loading YOLO model from {settings.MODEL_PATH}")
            model = YOLO(settings.MODEL_PATH)
            model.to(self.device)
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Could not load YOLO model: {e}")

    def detect(self, frame, draw=False):
        """
        Runs inference on a single frame.
        Returns a tuple: (detections, annotated_frame)
        detections: list of {'bbox': [x1, y1, x2, y2], 'conf': float, 'class': int}
        annotated_frame: frame with bounding boxes drawn (if draw=True)
        """
        if self.model is None:
            logger.error("Model not loaded.")
            return [], frame

        try:
            # Run inference
            results = self.model(frame, verbose=False, device=self.device, classes=[settings.TARGET_CLASS_ID], conf=settings.CONFIDENCE_THRESHOLD)
            
            detections = []
            annotated_frame = frame.copy() if draw else None

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    
                    bbox = [int(x1), int(y1), int(x2), int(y2)]
                    
                    detections.append({
                        "bbox": bbox,
                        "conf": conf,
                        "class": cls
                    })

                    if draw:
                        # Draw bounding box
                        cv2.rectangle(annotated_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                        label = f"{self.model.names[cls]} {conf:.2f}"
                        cv2.putText(annotated_frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            return detections, annotated_frame if draw else frame
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return [], frame
