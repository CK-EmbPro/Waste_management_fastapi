from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.waste_schema import WasteSchema
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.waste_model import WasteModel
from app.core.checkJwtPresence import JwtBearer
from app.core.decorators import role_required
from app.core.enums import Role, WasteCategory
from app.services import waste_service

router = APIRouter(prefix="wastes")


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_waste(add_waste_schema: WasteSchema, dependencies = Depends(JwtBearer()) , session:Session = Depends(get_session)):
    return waste_service.add_waste(add_waste_schema, dependencies, session)

@router.get('/', status_code=status.HTTP_200_OK)
def get_all_wastes(dependencies = Depends(JwtBearer()), session: Session = Depends(get_session)):
    return waste_service.get_all_wastes

@router.put('/{waste_id}', status_code=status.HTTP_202_ACCEPTED)
def edit_waste(waste_id : int, updated_waste: WasteSchema, session:Session = Depends(get_session), dependencies = Depends(JwtBearer())):
    return waste_service.edit_waste(waste_id, updated_waste, session, dependencies)
    
@router.delete('/{waste_id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_waste(waste_id: int, dependencies= Depends(JwtBearer()), session: Session = Depends(get_session)):
    return waste_service.delete_waste(waste_id, dependencies, session)
    
@router.get('/non_biodegradable')
@role_required([Role.NORMAL_USER])
def non_biodegradable_wastes(session: Session = Depends(get_session), dependencies = Depends(JwtBearer())):
    return waste_service.non_biodegradable_wastes(session, dependencies)
    
@router.get('/biodegradable')
@role_required([Role.NORMAL_USER])
def non_biodegradable_wastes(session: Session = Depends(get_session), dependencies = Depends(JwtBearer())):
    return waste_service.non_biodegradable_wastes(session, dependencies)
    
@router.get('/not_collected')
@role_required([Role.COLLECTOR])
def non_collected_wastes(session: Session = Depends(get_session), dependencies = Depends(JwtBearer())):
    return waste_service.non_collected_wastes(session, dependencies)
        
@router.get('collected')
@role_required([Role.COLLECTOR])
def collected_wastes(session: Session = Depends(get_session), dependencies = Depends(JwtBearer())):
    return waste_service.collected_wastes(session, dependencies)
        
        
@router.put('/{waste_id}/mark_collected', status)
def mark_collected(waste_id:int, session: Session= Depends(get_session), dependencies = Depends(JwtBearer())):
    return waste_service.mark_collected(waste_id, session, dependencies)