import models,schemas
from sqlalchemy.orm import Session

def get_user_by_username(db:Session,username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db:Session,db_user:models.User):
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user