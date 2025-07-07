from config.db_helper import database  # koneksi database async
from datetime import datetime

async def get_all_faces():
    query = "SELECT name, embedding FROM faces"
    return await database.fetch_all(query=query)

async def insert_face(name: str, embedding: str):
    query = """
        INSERT INTO faces (name, embedding, created_at)
        VALUES (:name, :embedding, :created_at)
    """
    try:
        values = {
            "name": name,
            "embedding": embedding,
            "created_at": datetime.utcnow()
        }
        return await database.execute(query=query, values=values)
    except Exception as e:
        print("DB Insert Error:", e)
        raise
