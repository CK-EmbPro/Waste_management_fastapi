from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta, timezone
from app.core.settings import settings
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"])
access_token_expire_minutes = settings.access_token_expire_minute
algorithm = settings.algorithm

def get_hashed_password(password):
    return password_context.hash(password)

def verify_password( password, hashed_password):
    return password_context.verify(password, hashed_password)

def create_jwt_access_token(subject: Union[str, Any], expires_timedelta:int = None):
    now = datetime.now(timezone.utc)
    if expires_timedelta:
        expires_timedelta = now + expires_timedelta
    else:
        expires_timedelta = now + timedelta(minutes=access_token_expire_minutes)
        
    payload_to_encode = {
        "exp": expires_timedelta,
        "sub": str(subject)
    }
    
    access_jwt_token = jwt.encode(payload_to_encode, access_token_expire_minutes, algorithm)
    
    return access_jwt_token

def create_jwt_refresh_token(subject: Union[str, Any], expires_timedelta:int = None):
    
    now = datetime.now(timezone.utc)
    
    if expires_timedelta:
        expires_timedelta = now + expires_timedelta
    else:
        expires_timedelta = now + timedelta(minutes=access_token_expire_minutes)
        
    payload_to_encode = {
        "exp": expires_timedelta,
        "sub": str(subject)
    }
    
    refresh_jwt_token = jwt.encode(payload_to_encode, access_token_expire_minutes, algorithm)
    
    return refresh_jwt_token