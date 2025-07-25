#AI-FRSS-DASH/be2/app/api/mobile_v1/endpoints/faces_api.py

from fastapi import APIRouter, HTTPException
from services.face_service import face_service
from schemas.faces_schemas import FaceEmbedding, FaceInsert

router = APIRouter()

@router.post("/verify")
async def verify_face(data: FaceEmbedding):
 """Verify face against database"""
 return await face_service.verify_face(data.embedding)

@router.post("/insert")
async def insert_face(data: FaceInsert):
 """Register new face"""
 return await face_service.register_face(data.name, data.embedding)