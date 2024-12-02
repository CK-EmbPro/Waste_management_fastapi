from fastapi import APIRouter, status, Depends, HTTPException
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



def register_user(user:UserSchema, session:Session):
    existing_user = session.query(UserModel).filter_by(email = user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    encrypted_password = get_hashed_password(user.password)
    new_user = UserModel(
        last_name = user.last_name,
        first_name = user.first_name,
        email= user.email,
        password = encrypted_password,
        phone_number = user.phone_number,
        role = user.role
    )
    
    session.add(new_user)
    session.commit()
    session.refresh()
    
    return {
        "message": "Registration successful",
        "user": new_user,
    }
    


def login_user(loginRequest: LoginSchema, session: Session):
    user = session.query(UserModel).filter_by(email = loginRequest.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Incorrect email")
    
    hashed_password = user.password
    
    is_password_correct = verify_password(loginRequest.password, hashed_password)
    
    if not is_password_correct:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Incorrect password")
    
    access_token = create_jwt_access_token(user.user_id)
    refresh_token = create_jwt_refresh_token(user.user_id)
    
    new_token = TokenModel(
        user_id = user.user_id,
        access_token = access_token,
        refresh_token = refresh_token,
        status = True
    )
    
    session.add(new_token)
    session.commit()
    session.close()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def logout_user(token:str, session: Session):
    token = token
    payload = jwt.decode(token, settings.jwt_access_secret_key, settings.algorithm)
    user_id = payload['sub']
    all_tokens = session.query(TokenModel).all()
    expired_tokens_user_ids = []
    
    now = datetime.now(timezone.utc)
    for token in all_tokens:
        if (now - token.created_date).days > 1:
            expired_tokens_user_ids.append(token)
            
    for expired_token_user_id in expired_tokens_user_ids:
        exp_token = session.query(TokenModel).where(user_id = expired_token_user_id).delete()
        session.commit()
    
    associated_token = session.query(TokenModel).filter(TokenModel.user_id==user_id, TokenModel.access_token == token).first()
    
    if associated_token:
        associated_token.status = False
        session.add(associated_token)
        session.commit()
        session.refresh(associated_token)        

    return {
        "message": "Logout successfully"
    }

def change_user_password(changePasswordRequest: ChangePassword, token:str, session: Session):
    user = session.query(UserModel).filter_by(email = changePasswordRequest.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    
    is_old_password_correct = verify_password(changePasswordRequest.old_password, user.password)
    
    if not is_old_password_correct:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password incorrect")
    
    encrypted_password = get_hashed_password(changePasswordRequest.new_password)
    user.password = encrypted_password
    session.commit()
    
    return {
        "message": "Password changed successfully",
        "user": user
    }
    
def get_all_users(token: str, session: Session):
    users = session.query(UserModel).all()
    return users

