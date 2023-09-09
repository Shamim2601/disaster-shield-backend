import models, schemas
from sqlalchemy.orm import Session


def get_all_services(db:Session):
    return db.query(models.Service).all()

def create_service(db:Session,service:schemas.Service_Create):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_service_by_service_id(db:Session,service_id:int):
    return db.query(models.Service).filter(models.Service.service_id==service_id).first()

def update_service(db:Session,service_id:int,service:schemas.Service_Update):
    values=service.dict(exclude_unset=True)
    db.query(models.Service).filter(models.Service.service_id==service_id) \
    .update(values,synchronize_session=False)
    db.commit()
    return get_service_by_service_id(db,service_id)
