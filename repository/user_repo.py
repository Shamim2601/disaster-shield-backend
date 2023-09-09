import models,schemas
from sqlalchemy.orm import Session

def get_user_by_username(db:Session,username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).get({"user_id":user_id})
    #return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_all_users(db: Session):
    # db.query(models.User).get()
    return db.query(models.User).all()
    

def create_user(db:Session,db_user:models.User):
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session,user_id:int,user:schemas.User_Update):
    values=user.dict(exclude_unset=True)
    # values.update({'hashed_password':hashed_password})
    db.query(models.User).filter(models.User.user_id==user_id) \
    .update(values,synchronize_session=False)
    db.commit()
    return get_user_by_id(db,user_id)

# def add_post(db:Session,post:schemas.Post_Create_Update):
#     db_post=models.Post(**post.dict(),creator_id=1,creation_time=0)
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post

# def get_all_posts(db:Session):
#     posts= db.query(models.Post).all()
#     print(posts[0].tags)
#     return posts