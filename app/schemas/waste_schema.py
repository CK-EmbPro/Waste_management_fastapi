from pydantic import BaseModel
from enum import Enum
from datetime import date
from app.core.enums import WasteCategory


    
class WasteSchema(BaseModel):
    category: WasteCategory
    weight: float
    date_collected: date
    description: str
    is_collected: bool