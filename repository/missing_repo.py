import models,schemas
from sqlalchemy.orm import Session
from datetime import datetime

def create_missing_person(db: Session, missing_person: schemas.Missing_Person_Create, user: models.User):
    creator_id = user.user_id
    creation_time = int(round(datetime.now().timestamp()))
    db_missing_person = models.Missing_Person(**missing_person.dict(exclude_unset=True), creator_id=creator_id, creation_time=creation_time)
    db.add(db_missing_person)
    db.commit()
    db.refresh(db_missing_person)
    return db_missing_person

def get_missing_person_by_id(db: Session, missing_person_id: int):
    return db.query(models.Missing_Person).filter(
        models.Missing_Person.missing_person_id == missing_person_id
    ).first()

def get_all_missing_persons(db: Session):
    return db.query(models.Missing_Person).all()

def update_missing_person(db: Session, missing_person_id: int, missing_person: schemas.Missing_Person_Update):
    db.query(models.Missing_Person).filter(
        models.Missing_Person.missing_person_id == missing_person_id
    ).update(missing_person.dict(exclude_unset=True), synchronize_session=False)

    db.commit()
    return get_missing_person_by_id(db, missing_person_id)
