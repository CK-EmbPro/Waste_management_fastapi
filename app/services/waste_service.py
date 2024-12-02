from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.waste_schema import WasteSchema
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.waste_model import WasteModel
from app.core.checkJwtPresence import JwtBearer
from app.core.decorators import role_required
from app.core.enums import Role, WasteCategory



def add_waste(add_waste_schema: WasteSchema, token: str , session:Session):
    try:
        new_waste = WasteModel(
            category = add_waste_schema.category,
            weight = add_waste_schema.weight,
            date_collected = add_waste_schema.date_collected,
            description = add_waste_schema.description,
            is_collected = add_waste_schema.is_collected
        )
    
        session.add(new_waste)
        session.commit()
        session.refresh(new_waste)
        
        return  {
            "message": "Waste added successfully",
            "data": new_waste
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_all_wastes(token:str, session: Session):
    all_wastes = session.query(WasteModel).all()
    return {
        "message": "Wastes retrieved successfully",
        "data": all_wastes
    }


def edit_waste(waste_id : int, updated_waste: WasteSchema, session:Session, token: str):
    try:
        waste_to_edit = session.query(WasteModel).filter(WasteModel.id == waste_id).first()
        
        if waste_to_edit is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Waste not found")
        
        waste_to_edit.category = updated_waste.category
        waste_to_edit.date_collected = updated_waste.date_collected
        waste_to_edit.description = updated_waste.description
        waste_to_edit.is_collected = updated_waste.is_collected
        waste_to_edit.weight = updated_waste.weight
        
        session.commit()
        session.refresh(waste_to_edit)
        
        return {
            "message": "Waste updated successfully",
            "data": waste_to_edit
        }
    except Exception as e:
        session.rollback()
        raise e
    finally: 
        session.close()


def delete_waste(waste_id: int, dependencies:str, session: Session):
    try:
        waste_to_delete = session.query(WasteModel).filter(WasteModel.id == waste_id).first()
        
        if not waste_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Waste to delete not found")
        
        session.delete(waste_to_delete)
        session.commit()
        
        return {
            "message": "Waste deleted successfully",
        }
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()

def non_biodegradable_wastes(session: Session, token: str):
    try:
        non_biodegradable_wastes_list = session.query(WasteModel).filter(WasteModel.category == WasteCategory.NON_BIODEGRADABLE).all()
        return {
            "message": "All non_biodegradable wastes",
            "data": non_biodegradable_wastes_list
        }
        
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()


def non_biodegradable_wastes(session: Session, token: str):
    try:
        biodegradable_wastes_list = session.query(WasteModel).filter(WasteModel.category == WasteCategory.BIODEGRADABLE).all()
        return {
            "message": "All non_biodegradable wastes",
            "data": biodegradable_wastes_list
        }
    
    except Exception as e:
        session.rollback()
        raise e 
    
    finally:
        session.close()

def non_collected_wastes(session: Session, token:str):
    try:
        non_yet_collected_wastes_list = session.query(WasteModel).filter(WasteModel.is_collected == False).all()
        return {
            "message": "All wastes note yet collected",
            "data": non_yet_collected_wastes_list
        }
        
    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()

def collected_wastes(session: Session, token:str):
    try:
        collected_wastes_list = session.query(WasteModel).filter(WasteModel.is_collected == True).all()
        return {
            "message": "All collected wastes",
            "data": collected_wastes_list
        }
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()

def mark_collected(waste_id:int, session: Session, token:str):
    try:
        waste_to_collect = session.query(WasteModel).filter(WasteModel.waste_id == waste_id).first()
        if not waste_to_collect:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Waste not found"
            )
            
        if waste_to_collect.is_collected:
            return {
                "message": "Waste already collected",
                "data": waste_to_collect
            }
            
        waste_to_collect.is_collected = True
        
        session.commit()
        
        return {
            "message": "Waste collected successfully",
            "data": waste_to_collect
        }
        
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()
