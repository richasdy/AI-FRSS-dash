import bcrypt
from datetime import datetime

# Asumsi: koneksi database menggunakan 'databases' atau 'aiomysql'
from config.db_helper import database  # sesuaikan dengan struktur kamu

async def get_admin_by_username(username: str):
    query = "SELECT * FROM admin WHERE username = :username"
    return await database.fetch_all(query=query, values={"username": username})

async def add_admin(username: str, password: str):
    query = """
        INSERT INTO admin (username, password, created_at)
        VALUES (:username, :password, :created_at)
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    values = {
        "username": username,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    return await database.execute(query=query, values=values)
