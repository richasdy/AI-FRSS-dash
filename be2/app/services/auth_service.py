import json
from app.models.auth import User, get_admin_by_username, add_admin
from app.services.database_service import database_service
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

async def handle_auth_ws_event(data: str) -> str:
    payload = json.loads(data)
    action = payload.get("action")
    
    if action == "signin":
        email = payload.get("email")
        password = payload.get("password")
        
        try:
            # Query user from database
            query = "SELECT * FROM users WHERE email = :email"
            result = await database_service.fetch_one(query, {"email": email})
            
            if result and result.get("password") == password:
                return json.dumps({
                    "status": "success", 
                    "message": "Signed in successfully",
                    "user": {
                        "id": result["id"],
                        "name": result.get("name", result.get("fullname")),
                        "email": result["email"],
                        "role_id": result.get("role_id")
                    }
                })
            else:
                return json.dumps({"status": "error", "message": "Invalid credentials"})
                
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Authentication failed: {str(e)}"})
            
    elif action == "register":
        name = payload.get("name") or payload.get("fullname")
        email = payload.get("email")
        password = payload.get("password")
        role_id = payload.get("role_id", 2)  # Default role
        
        try:
            # Insert new user
            query = """
            INSERT INTO users (name, email, password, role_id, created_at, updated_at)
            VALUES (:name, :email, :password, :role_id, datetime('now'), datetime('now'))
            """
            await database_service.execute_query(query, {
                "name": name,
                "email": email,
                "password": password,
                "role_id": role_id
            })
            
            return json.dumps({
                "status": "success",
                "message": "User registered successfully"
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Registration failed: {str(e)}"})
            
    else:
        return json.dumps({"status": "error", "message": "Unknown action"})
