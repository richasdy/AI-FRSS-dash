"""
Pydantic schemas for API validation and serialization.
"""

# Example: Base schema
from pydantic import BaseModel

class SchemaBase(BaseModel):
	class Config:
		orm_mode = True
