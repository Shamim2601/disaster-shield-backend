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

if __name__=="__main__":
    uvicorn.run("main:app",port=4001,reload=True)