from typing import Annotated

from pydantic import BaseModel,Field
from enum import Enum

class Dummy(BaseModel):
    id:int
    title:str=Field(...,max_length=20)
    class Config:
        orm_mode=True

class Image(BaseModel):
    # this unique image_id is the unique public_id in the cdn
    image_id:str=Field(...,max_length=255)
    # this url is the secure_id in the cdn
    url:str=Field(...,max_length=1000)
    
    class Config:
        orm_mode=True
    
    
    

class Access_Token(BaseModel):
    access_token: str
    token_type: str


class Access_Token_Data(BaseModel):
    username :str| None = None

class User_Base(BaseModel):
    first_name:str=Field(...,max_length=20,example='John')
    last_name:str=Field(...,max_length=20,example='Connor')
    latitude:float|None=Field(None,example=12)
    longitude:float|None=Field(None,example=12)
    
class User_Username(User_Base):
    username:str=Field(...,max_length=20,example='john123')

class User_Password(User_Base):
    password:str=Field(...,max_length=20,example='password')
    
class User_Create(User_Username,User_Password):
    pass

class User_Update(User_Password):
    pass

class User_Out(User_Username):
    user_id:int=Field(...,example=1)
    # image_id:int|None=Field(None)
    image:Image|None=Field(None)
    is_admin:bool=Field(False)   

class User(User_Out):
    hashed_password:str=Field(...,max_length=100,example='hashed password')
    class Config:
        orm_mode=True
        

class Post_Tag(BaseModel):
    tag:str=Field(...,max_length=20)
    post_id:int=Field(...)
    class Config:
        orm_mode=True

class Post_Base(BaseModel):
    title:str=Field(...,max_length=100)
    post_content:str|None=Field(None,max_length=1000)
    volunteers_needed:int|None=Field(None,gt=0)
    disaster_id:int|None=Field(None)
    
class Post_Create_Update(Post_Base):
    pass

class Post(Post_Base):
    post_id:int=Field(...)
    creation_time:int=Field(...)
    creator_id:int=Field(...)
    tags:list[Post_Tag]=Field(...)
    images:list[Image]=Field(...)
    class Config:
        orm_mode=True
        
class Disaster_Type(str,Enum):
    cyclone="cyclone"
    earthquake="earthquake"
    traffic_accident="traffic_accident"
    flood="flood"
    fire="fire"
    
       
class Disaster_Base(BaseModel):
    title:str=Field(...,max_length=100)
    disaster_type:Disaster_Type
    description:str|None=Field(None,max_length=1000)
    latitude:float|None=Field(None,example=12)
    longitude:float|None=Field(None,example=12)
    
class Disaster_Create(Disaster_Base):
    pass

class Disaster_Update(Disaster_Base):
    pass
    
class Disaster(Disaster_Base):
    disaster_id:int
    info_creation_time:int
    info_creator:User_Out
    class Config:
        orm_mode=True

class Missing_Person_Status(str,Enum):
    missing="missing"
    dead="dead"
    found="found"

class Gender(str,Enum):
    male="male"
    female="female"

class Missing_Person_Base(BaseModel):
    
    missing_person_name: str=Field(...,max_length=50)
    date_of_birth:int|None=Field(None)
    ethnicity: str|None=Field(None,max_length=20)
    gender: Gender|None=Field(None)
    weight_kg: int|None=Field(None,gt=0)
    height_cm: int|None=Field(None,gt=0)
    eye_color: str|None=Field(None,max_length=20)
    last_seen_time: int|None=Field(None)
    blood_group: str|None=Field(None,max_length=20)
    status: Missing_Person_Status
    circumstances: str|None=Field(None,max_length=500)
    phone:str|None=Field(None,max_length=30)
    address:str|None=Field(None,max_length=200)
    identifying_marks:str|None=Field(None,max_length=500)
    disaster_id: int

    
        
class Missing_Person_Create(Missing_Person_Base):
    pass

class Missing_Person_Update(Missing_Person_Base):
    pass

class Missing_Person(Missing_Person_Base):
    missing_person_id: int
    creator_id: int
    creation_time: int
    
    
    class Config:
        orm_mode = True

class Message_Base(BaseModel):
    content: str = Field(..., max_length=500,description="Content of the message")
    

class Message_Create(Message_Base):
    pass

class Message_Update(Message_Base):
    pass

class Message(Message_Base):
    message_id: int = Field(..., description="Unique ID of the message")
    sender_id: int = Field(..., description="ID of the message sender")
    conversation_id: int = Field(..., description="ID of the conversation")
    
    class Config:
        orm_mode = True 
 

class Conversation_Participant(BaseModel):
    participant_id: int = Field(..., description="Unique ID of the participant entry")
    conversation_id: int = Field(..., description="ID of the conversation")
    is_creator:bool
    class Config:
        orm_mode = True
 
        
class Conversation_Base(BaseModel):
    title: str = Field(..., max_length=100, description="Title of the conversation")

class Conversation_Create(Conversation_Base):
    is_group: bool = Field(..., description="Whether the conversation is a group conversation")
    pass

class Conversation_Update(Conversation_Base):
    pass

class Conversation(Conversation_Create):
    conversation_id: int = Field(..., description="Unique ID of the conversation")
    created_at: int = Field(..., description="Timestamp of conversation creation")
    messages:list[Message]=Field([])
    participants:list[Conversation_Participant]
    class Config:
        orm_mode = True

