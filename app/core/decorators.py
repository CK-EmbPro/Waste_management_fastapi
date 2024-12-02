from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.checkJwtPresence import JwtBearer
from functools import wraps
import jwt
from app.core.settings import settings
from app.core.database import get_session
from app.models.user_model import UserModel

def role_required(required_roles: list):
    def decorator(dependencies = Depends(JwtBearer()), session:Session =Depends(get_session)):
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                token = dependencies
                
                try:
                    payload = jwt.decode(token, settings.jwt_access_secret_key, settings.algorithm)
                except jwt.ExpiredSignatureError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Token is expired")
                except jwt.InvalidTokenError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
                
                user_id = payload['sub']
                if not user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid token payload"
                    )
                    
                user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail = "User not found"
                    )
                    
                if user.role not in required_roles:
                    raise HTTPException(
                        status_code= status.HTTP_400_BAD_REQUEST,
                        detail="No enough permission for the resource"
                    )
                    
                kwargs['user'] = user
                return func(*args, **kwargs)
            return inner
        return wrapper
    return decorator