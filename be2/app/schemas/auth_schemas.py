from pydantic import BaseModel

class AdminSignUp(BaseModel):
    username: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str
