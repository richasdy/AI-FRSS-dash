#AI-FRSS-DASH/be2/app/api/mobile_v1/endpoints/faces_api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.models import faces as model_face
from app.schemas.faces_schemas import FaceEmbedding, FaceInsert
import math

router = APIRouter()

# ---------- Utility Functions ----------
def calculate_euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def find_nearest(user_embedding, db_embeddings):
    best_match = None
    smallest_distance = float('inf')

    for row in db_embeddings:
        embedding_str = row.get("embedding")
        if not embedding_str:
            continue
        known_embedding = list(map(float, embedding_str.split(",")))
        if len(known_embedding) != len(user_embedding):
            continue

        distance = calculate_euclidean_distance(user_embedding, known_embedding)
        if distance < smallest_distance:
            smallest_distance = distance
            best_match = {
                "name": row.get("name"),
                "distance": distance
            }

    return best_match

# ---------- Routes ----------
@router.post("/verify")
async def verify_face(data: FaceEmbedding):
    if not isinstance(data.embedding, list):
        raise HTTPException(status_code=400, detail="Invalid or missing embedding")

    try:
        results = await model_face.get_all_faces()
        match = find_nearest(data.embedding, results)

        if match:
            return {
                "type": "recognize_face",
                "match": match["distance"] < 0.9,
                "name": match["name"],
                "distance": match["distance"]
            }
        else:
            return {
                "type": "recognize_face",
                "match": False,
                "name": None,
                "distance": None
            }
    except Exception as e:
        print("Verify face error:", e)
        raise HTTPException(status_code=500, detail="Server error during recognition")

@router.post("/insert")
async def insert_face(data: FaceInsert):
    try:
        embedding_string = ",".join(map(str, data.embedding))
        await model_face.insert_face(data.name, embedding_string)
        return {
            "type": "insert_face",
            "success": True
        }
    except Exception as e:
        print("Insert face error:", e)
        raise HTTPException(status_code=500, detail=str(e))