import models,schemas
from sqlalchemy.orm import Session


def get_all_disasters_by_title(db:Session, title:str):
    return db.query(models.Disaster).filter(models.Disaster.title == title).all()


def get_disaster_by_id(db:Session, disaster_id:int):
    return db.query(models.Disaster).filter(models.Disaster.disaster_id == disaster_id).first()


def get_all_disasters(db:Session):
    return db.query(models.Disaster).all()


def create_disaster(db:Session, db_disaster:models.Disaster):
    db.add(db_disaster)
    db.commit()
    db.refresh(db_disaster)
    return db_disaster

def update_disaster(db:Session, disaster_id:int, disaster:schemas.Disaster_Update):
    values=disaster.dict(exclude_unset=True)
    db.query(models.Disaster).filter(models.Disaster.disaster_id==disaster_id) \
    .update(values,synchronize_session=False)
    db.commit()
    return get_disaster_by_id(db,disaster_id)

# not needed. disasters wont be deleted in the app
def delete_disaster(db:Session, disaster_id:int):
    db.query(models.Disaster).filter(models.Disaster.disaster_id==disaster_id).delete()
    db.commit()
    return {"message":"Disaster deleted successfully"}