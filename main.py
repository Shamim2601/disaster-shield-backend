from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uvicorn


import models, schemas
from database import SessionLocal, engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db:Session=Depends(get_db)):
#     user = user_crud.get_user_by_name(db,token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# @app.post("/users", response_model=schemas.UserOut,tags=['User'])
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user_by_name(db,user.name)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return user_crud.create_user(db=db, user=user)


# @app.get("/users", response_model=list[schemas.UserOut],tags=['User'])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = user_crud.get_users(db, skip=skip, limit=limit)
#     return users

# @app.get("/users/me",tags=['User'])
# async def read_users_me(
#     current_user: Annotated[schemas.UserOut, Depends(get_current_user)]
# ):
#     # print(type(current_user))
#     return current_user

# @app.get("/users/{user_id}", response_model=schemas.UserOut,tags=['User'])
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/login",tags=['Log In'])
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)):
#     db_user=user_crud.get_user_by_name(db,form_data.username)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     if not form_data.password==db_user.password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": db_user.name, "token_type": "bearer"}

# @app.post('/missing',tags=['Missing Person'])
# async def create_missing(missing:schemas.MissingPersonCreate,current_user:
# Annotated[schemas.UserOut, Depends(get_current_user)],db:Session=Depends(get_db)):
#     missing:schemas.MissingPerson=missing_crud.create_missing(db,missing,current_user)
#     return missing
#     pass

# @app.get('/missing',tags=['Missing Person'])
# async def get_all_missing(db:Session=Depends(get_db)):
#     missing_array=missing_crud.get_all_missing(db)
#     return missing_array
#     pass


# @app.put('/missing/{missing_person_id}',tags=['Missing Person'])
# async def update_missing(missing_person_id:int,missing:schemas.MissingPersonCreate,current_user:
# Annotated[schemas.UserOut, Depends(get_current_user)],db:Session=Depends(get_db)):
#     db_missing=missing_crud.get_missing(db,missing_person_id)
#     if not db_missing:
#         raise HTTPException(status_code=400, detail="Missing Person does not exist")
#     if db_missing.added_by_id!=current_user.user_id:
#         raise HTTPException(status_code=400, detail="Unauthorized")
#     return missing_crud.update_missing(db,missing_person_id,missing,current_user)
#     pass


# User CRUD
@app.post('/users/', tags=['Users'], summary="Create a new user", response_model=schemas.User_Out)
async def create_user(user: schemas.User_Create_Update, db: Session = Depends(get_db)):
    pass

@app.get('/users/', tags=['Users'], summary="Get a list of users", response_model=list[schemas.User_Out])
async def list_users(db: Session = Depends(get_db)):
    pass

@app.get('/users/{user_id}', tags=['Users'], summary="Get user by ID", response_model=schemas.User_Out)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    pass

@app.put('/users/{user_id}', tags=['Users'], summary="Update user by ID", response_model=schemas.User_Out)
async def update_user(user_id: int, user: schemas.User_Create_Update, db: Session = Depends(get_db)):
    pass

# Post CRUD
@app.post('/posts/', tags=['Posts'], summary="Create a new post", response_model=schemas.Post)
async def create_post(post: schemas.Post_Create_Update, db: Session = Depends(get_db)):
    pass

@app.get('/posts/', tags=['Posts'], summary="Get a list of posts", response_model=list[schemas.Post])
async def list_posts(db: Session = Depends(get_db)):
    pass

@app.get('/posts/{post_id}', tags=['Posts'], summary="Get post by ID", response_model=schemas.Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    pass

@app.put('/posts/{post_id}', tags=['Posts'], summary="Update post by ID", response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.Post_Create_Update, db: Session = Depends(get_db)):
    pass

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


if __name__=="__main__":
    uvicorn.run("main:app",port=4001,reload=True)