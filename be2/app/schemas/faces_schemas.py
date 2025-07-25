from pydantic import BaseModel, validator
from typing import List, Optional

class FaceEmbedding(BaseModel):
    embedding: List[float]
    
    @validator('embedding')
    def validate_embedding(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Embedding cannot be empty')
        if len(v) < 128:
            raise ValueError('Embedding must contain at least 128 features')
        return v

class FaceInsert(BaseModel):
    name: str
    embedding: List[float]
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        if len(v.strip()) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip()
    
    @validator('embedding')
    def validate_embedding(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Embedding cannot be empty')
        if len(v) < 128:
            raise ValueError('Embedding must contain at least 128 features')
        return v

class FaceResponse(BaseModel):
 type: str
 match: bool
 name: Optional[str] = None
 distance: Optional[float] = None
 face_id: Optional[int] = None

class FaceInsertResponse(BaseModel):
 type: str
 success: bool
 message: str
 face_id: Optional[int] = None
