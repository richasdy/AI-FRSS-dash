import torch
from ultralytics import YOLO
import os
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class YOLOModelManager:
 """Manager untuk semua YOLO models"""
 
 def __init__(self, models_path: str = None):
 # Get models path from environment
 self.models_path = models_path or os.getenv("YOLO_MODELS_PATH", "yolo_models")
 self.loaded_models: Dict[str, YOLO] = {}
 
 # Get default confidence from environment
 self.default_confidence = float(os.getenv("DEFAULT_CONFIDENCE", "0.5"))
 
 self.model_configs = {
 "intrusion": {
 "file": "intrusion_yolov11.pt",
 "description": "Deteksi objek mencurigakan (barang tertinggal)",
 "classes": ["box", "suitcase"],
 "size_mb": 5.19,
 "architecture": "YOLO11n"
 },
 "people": {
 "file": "People_yolov8s_trained.pt", 
 "description": "Deteksi dan counting manusia",
 "classes": ["human"],
 "size_mb": 21.45,
 "architecture": "YOLOv8s"
 },
 "security_threats": {
 "file": "SecurityThreats_best_gun.pt",
 "description": "Deteksi senjata api",
 "classes": ["gun"],
 "size_mb": 49.61,
 "architecture": "Custom YOLO"
 },
 "vehicle": {
 "file": "vehicle_model_v11.pt",
 "description": "Klasifikasi jenis kendaraan",
 "classes": ["Ambulance", "Bus", "Car", "Motorcycle", "Truck"],
 "size_mb": 5.20,
 "architecture": "YOLO11n"
 }
 }
 
 def load_model(self, model_name: str) -> YOLO:
 """Load specific YOLO model"""
 if model_name in self.loaded_models:
 return self.loaded_models[model_name]
 
 if model_name not in self.model_configs:
 raise ValueError(f"Model {model_name} tidak tersedia. Available: {list(self.model_configs.keys())}")
 
 model_file = self.model_configs[model_name]["file"]
 model_path = os.path.join(self.models_path, model_file)
 
 if not os.path.exists(model_path):
 raise FileNotFoundError(f"Model file tidak ditemukan: {model_path}")
 
 try:
 model = YOLO(model_path)
 self.loaded_models[model_name] = model
 logger.info(f"Model {model_name} berhasil dimuat dari {model_path}")
 return model
 except Exception as e:
 logger.error(f"Error loading model {model_name}: {e}")
 raise
 
 def get_available_models(self) -> Dict[str, Dict]:
 """Dapatkan daftar model yang tersedia"""
 return self.model_configs
 
 def unload_model(self, model_name: str):
 """Unload model dari memory"""
 if model_name in self.loaded_models:
 del self.loaded_models[model_name]
 logger.info(f"Model {model_name} dihapus dari memory")
 
 def predict(self, model_name: str, image, **kwargs) -> List[Dict[str, Any]]:
 """Prediksi menggunakan model tertentu"""
 model = self.load_model(model_name)
 
 # Default parameters untuk inference
 default_params = {
 "conf": self.default_confidence, # Use confidence from .env
 "iou": 0.45, # IoU threshold for NMS
 "max_det": 100, # maximum detections
 "classes": None # filter by class
 }
 default_params.update(kwargs)
 
 try:
 results = model(image, **default_params)
 
 # Parse results
 detections = []
 for result in results:
 boxes = result.boxes
 if boxes is not None:
 for i in range(len(boxes)):
 detection = {
 "bbox": boxes.xyxy[i].cpu().numpy().tolist(), # [x1, y1, x2, y2]
 "confidence": float(boxes.conf[i].cpu().numpy()),
 "class_id": int(boxes.cls[i].cpu().numpy()),
 "class_name": model.names[int(boxes.cls[i].cpu().numpy())]
 }
 detections.append(detection)
 
 return detections
 except Exception as e:
 logger.error(f"Error during prediction with {model_name}: {e}")
 raise

 def predict_multi_model(self, image, models: List[str] = None, **kwargs) -> Dict[str, List[Dict[str, Any]]]:
 """Prediksi menggunakan multiple model sekaligus"""
 if models is None:
 models = list(self.model_configs.keys())
 
 # Default parameters untuk inference
 default_params = {
 "conf": 0.5,
 "iou": 0.45,
 "max_det": 100,
 "classes": None
 }
 default_params.update(kwargs)
 
 results = {}
 
 for model_name in models:
 try:
 detections = self.predict(model_name, image, **default_params)
 results[model_name] = detections
 logger.info(f"Model {model_name}: {len(detections)} detections")
 except Exception as e:
 logger.error(f"Error with model {model_name}: {e}")
 results[model_name] = []
 
 return results
 
 def get_combined_detections(self, multi_results: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
 """Gabungkan hasil dari multiple model"""
 combined = []
 
 for model_name, detections in multi_results.items():
 for detection in detections:
 # Add model source to detection
 detection["source_model"] = model_name
 detection["model_description"] = self.model_configs[model_name]["description"]
 combined.append(detection)
 
 return combined

# Global instance
yolo_manager = YOLOModelManager()
