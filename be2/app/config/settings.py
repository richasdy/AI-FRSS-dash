from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # YOLO Models Configuration
    yolo_models_path: str = "yolo_models"
    default_confidence: float = 0.5
    default_iou_threshold: float = 0.45
    max_detections: int = 100
    
    # Image Processing
    max_image_width: int = 1280
    max_image_height: int = 720
    allowed_image_formats: List[str] = ["jpg", "jpeg", "png", "bmp", "tiff"]
    
    # Performance
    preload_models: List[str] = ["intrusion"]
    model_cache_size: int = 4
    inference_device: str = "cpu"  # or 'cuda'
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Database (optional)
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    
    # Security (optional)
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
