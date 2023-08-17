import models,schemas
from sqlalchemy.orm import Session

# def get_user_image(user_id:int,db:Session):
#     user=db.query(models.User).filter(models.User.user_id==user_id).first()
#     if not user:
#         return None
#     image_id=user.image_id
#     if not image_id:
#         return None
#     image=db.query(models.Image).filter(models.Image.image_id==image_id).first()
#     return image

def add_image_to_user(user_id:int,image:schemas.Image,db:Session):
    user=db.query(models.User).filter(models.User.user_id==user_id).first()
    if user:
        user.image_id=image.image_id
        db.commit()
        
def get_image_by_id(image_id:str,db:Session):
    return db.query(models.Image).filter(models.Image.image_id==image_id).first()
        
def add_image_to_post(image_id:str,post_id:int,db:Session):
    image=get_image_by_id(image_id,db)
    if image:
        image.post_id=post_id
        db.commit()
        return image

def add_image(image:schemas.Image,db:Session):
    db_image=models.Image(**image.dict())
    db.add(db_image)
    db.commit()

def delete_image(image_id:str,db:Session):
    image=db.query(models.Image).filter(models.Image.image_id==image_id).first()
    db.delete(image)
    db.commit()
    pass
