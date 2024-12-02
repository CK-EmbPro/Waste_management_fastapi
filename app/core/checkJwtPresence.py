from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request, HTTPException, status
from app.core.settings import settings
from jose import jwt

jwt_access_secret_key = settings.jwt_access_secret_key
algorithm = settings.algorithm

class JwtBearer(HTTPBearer):
    def __init__(self, auto_error:bool = True):
        super(JwtBearer, self).__init__(auto_error)
        
        
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await  super(JwtBearer, self).__call__(request)
        
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Invalid credentials scheme")
            
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid token")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "No token available")        
        
    
    def verify_jwt(self, jwtToken:str) -> bool :
        try:
            payload = jwt.decode(jwtToken, jwt_access_secret_key, algorithm)
        except:
            payload = None
            
        if payload is None:
            return False
        else:
            return True
        
        
jwtBearer = JwtBearer()