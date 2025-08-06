"""
Universal YOLO Models Service
Supports: intrusion, people, security_threats, vehicle detection
Easy to extend for new models
"""
import os
import base64
import time
from io import BytesIO
import numpy as np
from PIL import Image
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
import logging

# Import YOLO dependencies
try:
    from ultralytics import YOLO
    import torch
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Warning: YOLO dependencies not available")

# Import database functions with fallback
try:
    from app.models.models import save_detection_result, get_detection_history, update_model_metadata
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    # Create dummy functions for graceful fallback
    async def save_detection_result(*args, **kwargs):
        pass
    async def get_detection_history(*args, **kwargs):
        return []
    async def update_model_metadata(*args, **kwargs):
        pass

logger = logging.getLogger(__name__)

class UniversalYOLOService:
    """Universal service for all YOLO models"""
    
    def __init__(self):
        self.models = {}  # Cache for loaded models
        self.model_configs = {
            "intrusion": {
                "file": "intrusion_yolov11.pt",
                "classes": ["person", "intrusion"]  # Will be loaded from model
            },
            "people": {
                "file": "People_yolov8s_trained.pt", 
                "classes": ["person"]
            },
            "security_threats": {
                "file": "SecurityThreats_best_gun.pt",
                "classes": ["gun", "knife", "weapon"]
            },
            "vehicle": {
                "file": "vehicle_model_v11.pt",
                "classes": ["car", "truck", "bus", "motorcycle"]
            }
        }
        # Use absolute path to models
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.models_path = os.path.join(os.path.dirname(current_dir), "yolo_models")
    
    def _get_model_path(self, model_type: str) -> str:
        """Get full path to model file"""
        config = self.model_configs.get(model_type)
        if not config:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return os.path.join(self.models_path, config["file"])
    
    async def load_model(self, model_type: str) -> bool:
        """Load specific YOLO model"""
        try:
            if not YOLO_AVAILABLE:
                raise ImportError("YOLO dependencies not available")
            
            if model_type in self.models:
                logger.info(f"Model {model_type} already loaded")
                return True
            
            model_path = self._get_model_path(model_type)
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # Load model
            model = YOLO(model_path)
            self.models[model_type] = model
            
            # Get actual class names from model
            if hasattr(model, 'names'):
                classes = list(model.names.values())
                self.model_configs[model_type]["classes"] = classes
                
                # Update database metadata (optional - silent fail if DB unavailable)
                if DATABASE_AVAILABLE:
                    try:
                        await update_model_metadata(model_type, self.model_configs[model_type]["file"], classes)
                    except Exception as db_error:
                        logger.debug(f"Database metadata update skipped for {model_type}: {db_error}")
                        pass
            
            logger.info(f"Model {model_type} loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model {model_type}: {str(e)}")
            return False
    
    def _decode_image(self, image_data: str) -> Image.Image:
        """Decode base64 image data"""
        try:
            # Remove data URL prefix if present
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            return image
            
        except Exception as e:
            raise ValueError(f"Invalid image data: {str(e)}")
    
    async def detect_objects(self, model_type: str, image_data: str, 
                           confidence: float = 0.5, iou_threshold: float = 0.45) -> Dict[str, Any]:
        """Universal object detection for any model type"""
        try:
            start_time = time.time()
            
            # Load model if not loaded
            if model_type not in self.models:
                success = await self.load_model(model_type)
                if not success:
                    raise HTTPException(status_code=500, detail=f"Failed to load model: {model_type}")
            
            model = self.models[model_type]
            
            # Decode image
            image = self._decode_image(image_data)
            image_size = [image.width, image.height]
            
            # Run inference
            results = model(image, conf=confidence, iou=iou_threshold, verbose=False)
            
            # Process results
            detections = []
            if results and len(results) > 0:
                result = results[0]
                if hasattr(result, 'boxes') and result.boxes is not None:
                    boxes = result.boxes
                    for i in range(len(boxes)):
                        box = boxes.xyxy[i].cpu().numpy()  # [x1, y1, x2, y2]
                        conf = float(boxes.conf[i].cpu().numpy())
                        cls_id = int(boxes.cls[i].cpu().numpy())
                        
                        # Get class name
                        class_name = model.names[cls_id] if hasattr(model, 'names') else f"class_{cls_id}"
                        
                        detection = {
                            "class_id": cls_id,
                            "class_name": class_name,
                            "confidence": conf,
                            "bbox": box.tolist()
                        }
                        detections.append(detection)
            
            processing_time = time.time() - start_time
            
            # Save to database (optional - silent fail if DB unavailable)
            if DATABASE_AVAILABLE:
                try:
                    await save_detection_result(
                        model_type=model_type,
                        detections=detections,
                        processing_time=processing_time,
                        confidence=confidence,
                        iou=iou_threshold,
                        image_size=image_size
                    )
                except Exception as db_error:
                    logger.debug(f"Database save skipped for {model_type}: {db_error}")
                    pass
            
            return {
                "success": True,
                "model_type": model_type,
                "detections": detections,
                "total_detections": len(detections),
                "processing_time": processing_time,
                "image_size": image_size
            }
            
        except Exception as e:
            logger.error(f"Error in object detection: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")
    
    async def get_model_info(self, model_type: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        try:
            config = self.model_configs.get(model_type)
            if not config:
                raise ValueError(f"Unknown model type: {model_type}")
            
            return {
                "model_type": model_type,
                "model_file": config["file"],
                "classes": config["classes"],
                "loaded": model_type in self.models,
                "path": self._get_model_path(model_type)
            }
            
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def list_all_models(self) -> Dict[str, Any]:
        """List all available models"""
        try:
            models_info = []
            for model_type in self.model_configs.keys():
                info = await self.get_model_info(model_type)
                models_info.append(info)
            
            return {
                "success": True,
                "models": models_info,
                "total_models": len(models_info)
            }
            
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_detection_history(self, model_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get detection history from database"""
        try:
            history = await get_detection_history(model_type, limit)
            return history
            
        except Exception as e:
            logger.error(f"Error getting detection history: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

# Global service instance
yolo_service = UniversalYOLOService()
