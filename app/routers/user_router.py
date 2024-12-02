from fastapi import APIRouter, status, Depends, HTTPException
from app.core.database import get_session
from app.schemas.user_schema import UserSchema, LoginSchema, ChangePassword
from app.models.user_model import UserModel
from app.models.token_model import TokenModel
from sqlalchemy.orm import Session
from app.core.utils import get_hashed_password, verify_password, create_jwt_access_token, create_jwt_refresh_token
from app.core.checkJwtPresence import JwtBearer
from app.schemas.token_schema import TokenSchema
from app.core.settings import settings
import jwt
from datetime import datetime, timezone
from app.services import user_service

router = APIRouter(prefix="users", tags=['Users'])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user:UserSchema, session:Session = Depends(get_session)):
    return user_service.register_user(user,session)
    

@router.post('/login',response_model= TokenSchema , status_code=status.HTTP_201_CREATED)
def login(loginRequest: LoginSchema, session: Session = Depends(get_session)):
    return user_service.login_user(loginRequest,session)
    
@router.post("/logout", status_code=status.HTTP_201_CREATED)
def logout(dependencies = Depends(JwtBearer()), session: Session = Depends(get_session)):
    return user_service.logout_user(dependencies, session)
    
    

@router.put('/change_password', status_code=status.HTTP_202_ACCEPTED)
def change_password(changePasswordRequest: ChangePassword, dependencies = Depends(JwtBearer()), session: Session = Depends(get_session)):
    return user_service.change_user_password(changePasswordRequest,dependencies, session)
    

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(dependencies = Depends(JwtBearer), session: Session = Depends(get_session)):
    return user_service.get_all_users(dependencies)

