from app.core.database import Base
from enum import Enum
from sqlalchemy import Column, Integer, Boolean, Float, Date, String
from app.core.enums import WasteCategory

class WasteModel(Base):
    __tablename__ = "wastes"
    waste_id = Column(Integer, primary_key= True)
    category = Column(Enum(WasteCategory), nullable = False)
    weight = Column(Float, nullable = False)
    date_collected = Column(Date, nullable = False)
    description = Column(String(30), nullable = False)
    is_collected = Column(Boolean, nullable = False)