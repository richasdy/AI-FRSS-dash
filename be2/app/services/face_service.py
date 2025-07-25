"""
Face Recognition Service
Handles face verification and registration
"""
import numpy as np
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
import logging

# from models.database_models import Face  # Uncomment when database is connected
# from services.database_service import database_service  # Uncomment when needed

logger = logging.getLogger(__name__)

class FaceService:
    """Face recognition and management service"""
    
    def __init__(self):
        self.similarity_threshold = 0.6  # Euclidean distance threshold
    
    async def register_face(self, name: str, embedding: List[float]) -> Dict[str, Any]:
        """Register new face with embedding"""
        try:
            # Convert embedding to string for storage
            embedding_str = ",".join(map(str, embedding))
            
            # Create new face record (uncomment when database is connected)
            # new_face = Face(
            #     name=name,
            #     embedding=embedding_str
            # )
            
            # Save to database (would need actual database connection)
            # For now, return success response
            return {
                "type": "face_insert",
                "success": True,
                "message": f"Face for {name} registered successfully",
                "face_id": "temp_id"  # Would be actual ID from database
            }
            
        except Exception as e:
            logger.error(f"Error registering face: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to register face: {str(e)}")
    
    async def verify_face(self, embedding: List[float]) -> Dict[str, Any]:
        """Verify face against registered faces"""
        try:
            # Convert input embedding to numpy array
            input_embedding = np.array(embedding)
            
            # Get all registered faces from database
            # For now, return mock response
            
            return {
                "type": "face_verification",
                "success": False,
                "message": "No matching face found",
                "similarity": 0.0,
                "matched_name": None
            }
            
        except Exception as e:
            logger.error(f"Error verifying face: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to verify face: {str(e)}")
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate euclidean distance similarity between two embeddings"""
        try:
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Calculate euclidean distance
            distance = np.linalg.norm(emb1 - emb2)
            
            # Convert to similarity score (lower distance = higher similarity)
            similarity = 1.0 / (1.0 + distance)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    async def get_all_faces(self) -> List[Dict[str, Any]]:
        """Get all registered faces"""
        try:
            # Would get from database
            # For now, return empty list
            return []
            
        except Exception as e:
            logger.error(f"Error getting faces: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get faces: {str(e)}")
    
    async def delete_face(self, face_id: str) -> Dict[str, Any]:
        """Delete a registered face"""
        try:
            # Would delete from database
            # For now, return success response
            return {
                "type": "face_delete",
                "success": True,
                "message": f"Face {face_id} deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting face: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to delete face: {str(e)}")

# Global face service instance
face_service = FaceService()
