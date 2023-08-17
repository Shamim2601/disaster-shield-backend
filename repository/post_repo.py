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
        
