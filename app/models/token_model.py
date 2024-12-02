from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class TokenModel(Base):
    __tablename__ = 'token'
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default = datetime.datetime.now)