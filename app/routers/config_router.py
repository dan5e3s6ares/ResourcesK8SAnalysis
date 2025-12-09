from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models, schemas
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/configurations", tags=["configurations"])


@router.post("/", response_model=schemas.Configuration)
def create_configuration(
    config: schemas.ConfigurationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_config = models.Configuration(
        **config.dict(),
        user_id=current_user.id
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


@router.get("/", response_model=List[schemas.Configuration])
def list_configurations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Configuration).filter(
        models.Configuration.user_id == current_user.id
    ).all()


@router.get("/{config_id}", response_model=schemas.Configuration)
def get_configuration(
    config_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config = db.query(models.Configuration).filter(
        models.Configuration.id == config_id,
        models.Configuration.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return config


@router.put("/{config_id}", response_model=schemas.Configuration)
def update_configuration(
    config_id: int,
    config_update: schemas.ConfigurationUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config = db.query(models.Configuration).filter(
        models.Configuration.id == config_id,
        models.Configuration.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    update_data = config_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)
    
    db.commit()
    db.refresh(config)
    return config


@router.delete("/{config_id}")
def delete_configuration(
    config_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config = db.query(models.Configuration).filter(
        models.Configuration.id == config_id,
        models.Configuration.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    db.delete(config)
    db.commit()
    return {"message": "Configuration deleted successfully"}
