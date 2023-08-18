from typing import Annotated,Optional

from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from repository import user_repo,image_repo,post_repo
import uvicorn
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile,Query,Body,Path,File,Form

from dotenv import load_dotenv
import os

import models, schemas
from database import SessionLocal, engine
from datetime import timedelta,datetime
from jose import JWTError,jwt
from image_service import image_service


load_dotenv()

ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_ALGORITHM = os.getenv('ACCESS_TOKEN_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 180

origins=[
    "http://localhost:4200"
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/")
async def hello():
    return {"msg":"hello"}


# Password Hashing
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Authentication

## Token Creation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt


# Authentication Routes
@app.post('/login',tags=['Authentication'],summary='Log In')
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user=user_repo.get_user_by_username(db,form_data.username)
    if not user:
        raise HTTPException(status_code=400,detail='Incorrect credentialss')
    if not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400,detail='Incorrect credentials')

    access_token_expire=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token({"sub":user.username},expires_delta=access_token_expire)
    return {"access_token":access_token,"token_type":"bearer"}
    


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        # apparently "sub" i.e. "subject" is recommended
        # as a claim than "username" , but not necessary, you can put anything
        ## claims are statements about an entity (typically, the user)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.Access_Token_Data(username=username)
    except JWTError:
        raise credentials_exception
    user=user_repo.get_user_by_username(db,token_data.username)
    if not user:
        raise credentials_exception
    return user




# User CRUD
@app.get('/users/me',tags=['Users'],summary='Get Current User',response_model=schemas.User_Out)
async def send_current_user(current_user:Annotated[models.User,Depends(get_current_user)]):
    return current_user

@app.post('/user/{user_id}/image',tags=['Users'],response_model=schemas.Image)
async def upload_user_image(user_id:int,file:UploadFile,\
    current_user:Annotated[models.User,Depends(get_current_user)],db:Session=Depends(get_db)):

    if current_user.user_id!=user_id:
        raise HTTPException(status_code=401,detail='Unauthorized')
    if file.content_type!='image/jpeg':
        raise HTTPException(status_code=400,detail='Image Format Not Supported')
    
    if current_user.image_id:
        image_id:str=current_user.image_id
        image_service.deleteImage(image_id)
        image_repo.delete_image(image_id,db)
            
    image:schemas.Image= image_service.uploadImage(file.file.read(),folder_name='/users')
    image_repo.add_image(image,db)
    image_repo.add_image_to_user(current_user.user_id,image,db)
    return image    

@app.post('/users/', tags=['Users'], summary="Create a new user", response_model=schemas.User_Out)
async def create_user(user: schemas.User_Create, db: Session = Depends(get_db)):
    db_user=user_repo.get_user_by_username(db,user.username)
    if db_user:
        raise HTTPException(status_code=400,detail='username is taken')
    hashed_password=get_password_hash(user.password)
    is_admin=False
    db_user=models.User(**user.dict(exclude=['password']),hashed_password=hashed_password,is_admin=is_admin)
    return user_repo.create_user(db,db_user)

@app.get('/users/', tags=['Users'], summary="Get a list of users", response_model=list[schemas.User_Out])
async def list_users(db: Session = Depends(get_db)):
    return user_repo.get_all_users(db)

@app.get('/users/{user_id}', tags=['Users'], summary="Get user by ID", response_model=schemas.User_Out)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user=user_repo.get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=404,detail='user not found')
    return user
    pass



@app.put('/users/{user_id}', tags=['Users'], summary="Update user by ID", response_model=schemas.User_Out)
async def update_user(user_id: int, user: schemas.User_Update, crnt_usr: Annotated[models.User, Depends(get_current_user)] , \
    db: Session = Depends(get_db)):
    
    if crnt_usr.user_id != user_id:
        raise HTTPException(status_code=400,detail="You can't edit ohter's profile")
    db_user=user_repo.get_user_by_id(db,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail='user not found')
    hashed_password=get_password_hash(user.password)
    
    return user_repo.update_user(db,user_id,hashed_password,user)



# Post CRUD
@app.post('/posts/', tags=['Posts'], summary="Create a new post", response_model=schemas.Post)
async def create_post(post: schemas.Post_Create,user:Annotated[models.User,Depends(get_current_user)], \
    db: Session = Depends(get_db)):
    
    #TODO : Check if the disaster_id in the post exists
    
    return post_repo.create_post(db,post,user)
    pass

@app.get('/posts/', tags=['Posts'], summary="Get a list of posts", response_model=list[schemas.Post])
async def list_posts(db: Session = Depends(get_db)):
    return post_repo.get_all_posts(db)

@app.get('/posts/{post_id}', tags=['Posts'], summary="Get post by ID", response_model=schemas.Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post=post_repo.get_post_by_id(db,post_id)
    if not db_post:
        raise HTTPException(status_code=404,detail='post not found')
    return db_post

@app.put('/posts/{post_id}', tags=['Posts'], summary="Update post by ID", response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.Post_Update,user:Annotated[models.User,Depends(get_current_user)],\
    db: Session = Depends(get_db)):
    
    db_post:models.Post=post_repo.get_post_by_id(db,post_id)
    if not db_post:
         raise HTTPException(status_code=404,detail='post not found')
    if db_post.creator_id!=user.user_id:
         raise HTTPException(status_code=401,detail='you cannot edit this post')
    return post_repo.update_post(db,post_id,post)

@app.post('/posts/{post_id}/image',tags=['Posts'], summary="add image to post", response_model=schemas.Image)
async def upload_post_images(post_id:int,file:UploadFile,\
    current_user:Annotated[models.User,Depends(get_current_user)],db:Session=Depends(get_db)):
    
    db_post:models.Post=post_repo.get_post_by_id(db,post_id)
    if not db_post:
         raise HTTPException(status_code=404,detail='post not found')
    if current_user.user_id!=db_post.creator_id:
        raise HTTPException(status_code=401,detail='Unauthorized')
    if file.content_type!='image/jpeg':
        raise HTTPException(status_code=400,detail='Image Format Not Supported')
    
            
    image:schemas.Image= image_service.uploadImage(file.file.read(),folder_name='/posts')
    image_repo.add_image(image,db)
    return image_repo.add_image_to_post(image.image_id,db_post.post_id,db)

@app.delete('/posts/{post_id}/image',tags=['Posts'], summary="delete image to post")
async def delete_post_image(post_id:int,image_id:Annotated[str,Query(...,max_length=255)],\
    current_user:Annotated[models.User,Depends(get_current_user)],db:Session=Depends(get_db)):
    db_post:models.Post=post_repo.get_post_by_id(db,post_id)
    if not db_post:
        raise HTTPException(status_code=404,detail='post not found')
    if current_user.user_id!=db_post.creator_id:
        raise HTTPException(status_code=401,detail='Unauthorized')
    db_image=image_repo.get_image_by_id(image_id,db)
    if not db_image or db_image.post_id!=db_post.post_id:
        raise HTTPException(status_code=404,detail='image not found')
    image_service.deleteImage(image_id)
    db.delete(db_image)
    db.commit()

@app.post('/posts/{post_id}/enlist',tags=['Posts'], summary="enlist to the volunteership")
async def enlist_to_post(post_id:int,current_user:Annotated[models.User,Depends(get_current_user)],\
    db:Session=Depends(get_db)):
    
    db_post:models.Post=post_repo.get_post_by_id(db,post_id)
    if not db_post:
        raise HTTPException(status_code=404,detail='post not found')
    
    post_enlistment=post_repo.get_post_enlistment(db,post_id,current_user.user_id)
    if post_enlistment:
        raise HTTPException(status_code=400,detail='already enlisted')
    return post_repo.add_post_enlistment(db,post_id,current_user.user_id)

@app.delete('/posts/{post_id}/enlist', tags=['Posts'], summary="De-enlist from the volunteership")
async def de_enlist_from_post(post_id: int, current_user: models.User = Depends(get_current_user), 
                              db: Session = Depends(get_db)):
    db_post = post_repo.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail='Post not found')

    post_enlistment = post_repo.get_post_enlistment(db, post_id, current_user.user_id)
    if not post_enlistment:
        raise HTTPException(status_code=400, detail='Not enlisted')
    
    db.delete(post_enlistment)
    db.commit()
 
@app.post('/posts/{post_id}/tags', tags=['Posts'], summary="add tag to post", response_model=schemas.Post_Tag)
async def add_tag_to_post(post_id: int, tag:Annotated[str,Query(...,max_length=20)],\
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = post_repo.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail='Post not found')
    if current_user.user_id != db_post.creator_id:
        raise HTTPException(status_code=401, detail='Unauthorized')
    db_post_tag=post_repo.get_post_tag(db,post_id,tag)
    if db_post_tag:
        raise HTTPException(status_code=400, detail='tag already exists')
    
    tag_obj = post_repo.add_tag_to_post(db,schemas.Post_Tag(tag=tag,post_id=post_id))
    return tag_obj

@app.delete('/posts/{post_id}/tags', tags=['Posts'], summary="remove tag from post")
async def remove_tag_from_post(post_id: int, tag: str,\
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = post_repo.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail='Post not found')
    if current_user.user_id != db_post.creator_id:
        raise HTTPException(status_code=401, detail='Unauthorized')
    
    post_repo.remove_tag_from_post(db, post_id, tag)

@app.post('/posts/{post_id}/report', tags=['Posts'], summary="Report a post")
async def report_post(post_id: int,\
    current_user: Annotated[models.User, Depends(get_current_user)],\
    report_reason: schemas.Post_Report_Reason,\
    db: Session = Depends(get_db)):
    
    db_post: models.Post = post_repo.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail='Post not found')

    existing_report = post_repo.get_post_report(db, post_id, current_user.user_id)
    if existing_report:
        raise HTTPException(status_code=400, detail='Already reported')

    return post_repo.submit_post_report(db, post_id, current_user.user_id, report_reason) 

# TODO make upload File Optional
@app.post('/posts/{post_id}/comment', tags=['Posts'], summary="Add a comment")#response_model=schemas.Post_Comment)
async def add_comment_to_post(post_id: int, 
    current_user: Annotated[models.User, Depends(get_current_user)],file:UploadFile,\
    content:Annotated[str|None,Form(...,max_length=500)],\
    db: Session = Depends(get_db),):
    
    db_post = post_repo.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    if file.content_type!='image/jpeg':
        raise HTTPException(status_code=400,detail='Image Format Not Supported')
    image:schemas.Image= image_service.uploadImage(file.file.read(),folder_name='/comments')
    image_repo.add_image(image,db)
    commenter_id=current_user.user_id
    image_id=image.image_id
    created_at=int(round(datetime.now().timestamp()))
    
    comment=models.Post_Comment(commenter_id=commenter_id,image_id=image_id,\
    created_at=created_at,content=content,post_id=post_id)
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    print(comment.image)
    return comment
    
    # comment_data = comment.dict()
    # comment_data["commenter_id"] = current_user.user_id
    # comment_data["post_id"] = post_id
    # comment_data["time"] = int(round(datetime.utcnow().timestamp()))
    # return comment_data
    #return post_repo.add_comment_to_post(db, schemas.Post_Comment_Create(**comment_data))


# Disaster CRUD
@app.post('/disasters/', tags=['Disasters'], summary="Create a new disaster", response_model=schemas.Disaster)
async def create_disaster(disaster: schemas.Disaster_Create, db: Session = Depends(get_db)):
    pass

@app.get('/disasters/', tags=['Disasters'], summary="Get a list of disasters", response_model=list[schemas.Disaster])
async def list_disasters(db: Session = Depends(get_db)):
    pass

@app.get('/disasters/{disaster_id}', tags=['Disasters'], summary="Get disaster by ID", response_model=schemas.Disaster)
async def read_disaster(disaster_id: int, db: Session = Depends(get_db)):
    pass

@app.put('/disasters/{disaster_id}', tags=['Disasters'], summary="Update disaster by ID", response_model=schemas.Disaster)
async def update_disaster(disaster_id: int, disaster: schemas.Disaster_Update, db: Session = Depends(get_db)):
    pass

# Missing Person CRUD
@app.post('/missing/', tags=['Missing Person'], summary="Create a new missing person report", response_model=schemas.Missing_Person)
async def create_missing(missing: schemas.Missing_Person_Create, db: Session = Depends(get_db)):
    pass

@app.get('/missing/', tags=['Missing Person'], summary="Get a list of missing persons", response_model=list[schemas.Missing_Person])
async def list_missing_persons(db: Session = Depends(get_db)):
    pass

@app.get('/missing/{missing_person_id}', tags=['Missing Person'], summary="Get missing person by ID", response_model=schemas.Missing_Person)
async def read_missing(missing_person_id: int, db: Session = Depends(get_db)):
    pass

@app.put('/missing/{missing_person_id}', tags=['Missing Person'], summary="Update missing person by ID", response_model=schemas.Missing_Person)
async def update_missing(missing_person_id: int, missing: schemas.Missing_Person_Update, db: Session = Depends(get_db)):
    pass


# Conversation CRUD
@app.post('/messages/conversations/', tags=['Messages'], summary="Create a new conversation", response_model=schemas.Conversation)
async def create_conversation(conversation: schemas.Conversation_Create, db: Session = Depends(get_db)):
    pass

@app.get('/messages/conversations/', tags=['Messages'], summary="Get a list of conversations", response_model=list[schemas.Conversation])
async def list_conversations(db: Session = Depends(get_db)):
    pass

@app.get('/messages/conversations/{conversation_id}', tags=['Messages'], summary="Get conversation by ID", response_model=schemas.Conversation)
async def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    pass

@app.put('/messages/conversations/{conversation_id}', tags=['Messages'], summary="Update conversation by ID", response_model=schemas.Conversation)
async def update_conversation(conversation_id: int, conversation: schemas.Conversation_Update, db: Session = Depends(get_db)):
    pass

# Message CRUD
@app.post('/messages/', tags=['Messages'], summary="Send a new message", response_model=schemas.Message)
async def send_message(message: schemas.Message_Create, db: Session = Depends(get_db)):
    pass

@app.put('/messages/{message_id}', tags=['Messages'], summary="Edit a message by ID", response_model=schemas.Message)
async def edit_message(message_id: int, message: schemas.Message_Update, db: Session = Depends(get_db)):
    pass

@app.get('/messages/user/{user_id}', tags=['Messages'], summary="Get all messages of a user", response_model=list[schemas.Message])
async def list_user_messages(user_id: int, db: Session = Depends(get_db)):
    pass

# Conversation Participants CRUD
@app.post('/messages/participants/', tags=['Messages'], summary="Add a participant to a conversation", response_model=schemas.Conversation_Participant)
async def add_participant(participant: schemas.Conversation_Participant, db: Session = Depends(get_db)):
    pass

@app.get('/messages/participants/conversation/{conversation_id}', tags=['Messages'], summary="Get all participants of a conversation", response_model=list[schemas.Conversation_Participant])
async def list_conversation_participants(conversation_id: int, db: Session = Depends(get_db)):
    pass

# @app.post('/post_test')
# async def post_test(post:schemas.Post_Create_Update,db:Session=Depends(get_db)):
#     return user_repo.add_post(db,post)

# @app.get('/all_posts_test')
# async def post_all(db:Session=Depends(get_db)):
#     return user_repo.get_all_posts(db)

if __name__=="__main__":
    uvicorn.run("main:app",port=4001,reload=True,host="0.0.0.0")