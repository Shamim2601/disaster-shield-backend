import models,schemas
from sqlalchemy.orm import Session
from datetime import datetime

def get_all_posts(db:Session):
    pass

def create_post(db:Session,post:schemas.Post_Create,user:models.User):
    creator_id=user.user_id
    creation_time=int(round(datetime.now().timestamp()))
    db_post=models.Post(**post.dict(),creator_id=creator_id,creation_time=creation_time)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post_by_id(db:Session,post_id:int):
    return db.query(models.Post).filter(\
        models.Post.post_id == post_id).first()
    
def get_all_posts(db:Session):
    return db.query(models.Post).all()

def update_post(db:Session,post_id:int,post:schemas.Post_Update):
    db.query(models.Post).filter(models.Post.post_id\
    == post_id).update(post.dict(exclude_unset=True),\
    synchronize_session=False)
    
    db.commit()
    return get_post_by_id(db,post_id)

def get_post_tag(db:Session,post_id:int,tag:str):
    return db.query(models.Post_Tag)\
        .filter(models.Post_Tag.post_id == post_id,
        models.Post_Tag.tag == tag).first()

def add_tag_to_post(db: Session, post_tag:schemas.Post_Tag):
        tag_obj = models.Post_Tag(**post_tag.dict())
        db.add(tag_obj)
        db.commit()
        db.refresh(tag_obj)
        return tag_obj

def remove_tag_from_post(db: Session, post_id: int, tag: str):
    db.query(models.Post_Tag).filter(
        models.Post_Tag.post_id == post_id,
        models.Post_Tag.tag == tag
    ).delete(synchronize_session=False)
    db.commit()
    
def get_post_enlistment(db:Session,post_id:int,user_id:int):
    return db.query(models.Post_Enlistment).filter(
        models.Post_Enlistment.post_id == post_id,
        models.Post_Enlistment.user_id == user_id
    ).first()

def add_post_enlistment(db:Session,post_id:int,user_id:int):
    post_enlistment=models.Post_Enlistment(post_id=post_id,user_id=user_id)
    db.add(post_enlistment)
    db.commit()
    db.refresh(post_enlistment)
    return post_enlistment

def submit_post_report(db: Session, post_id: int, user_id: int, report_reason: schemas.Post_Report_Reason):
    report = models.Post_Report(post_id=post_id, user_id=user_id, report_reason=report_reason)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_all_post_reports(db: Session):
    return db.query(models.Post_Report).all()

def get_post_report(db: Session, post_id: int, user_id: int):
    return db.query(models.Post_Report).filter(
        models.Post_Report.post_id == post_id,
        models.Post_Report.user_id == user_id
    ).first()
