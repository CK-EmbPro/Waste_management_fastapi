from pydantic import BaseModel, EmailStr
from app.core.enums import Role


class UserSchema(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    phone_number: int
    role: Role
    
class LoginSchema(BaseModel):
    username: str
    email: str
    password: str
    
    
    
class ChangePassword(BaseModel):
    email:str
    old_password: str
    new_password: str
    