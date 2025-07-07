import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Buat koneksi ke database
db_config = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def get_connection():
    return mysql.connector.connect(**db_config)
