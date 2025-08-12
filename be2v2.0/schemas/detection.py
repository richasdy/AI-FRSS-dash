from pydantic import BaseModel
from typing import List, Any

class DetectionRequest(BaseModel):
    image_data: str
    model_type: str

class DetectionResult(BaseModel):
    class_name: str
    confidence: float
    bbox: list

class DetectionResponse(BaseModel):
    detections: List[DetectionResult]
    model_type: str
    success: bool = True
