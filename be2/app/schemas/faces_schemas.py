from pydantic import BaseModel
from typing import List

class FaceEmbedding(BaseModel):
    embedding: List[float]

class FaceInsert(BaseModel):
    name: str
    embedding: List[float]
