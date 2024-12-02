from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date
from app.core.enums import Role
from enum import Enum



class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True)
    last_name = Column(String(30), nullable= False)
    first_name = Column(String(30), nullable= False)
    email= Column(String(50), unique = True, nullable= False)
    password = Column(String(30), nullable= False)
    phone_number = Column(Integer, nullable= False)
    role = Column(Enum(Role), nullable= False)