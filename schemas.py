from typing import Annotated

from pydantic import BaseModel,Field
from enum import Enum

# class Dummy(BaseModel):
#     id:int
#     title:str=Field(...,max_length=20)
#     class Config:
#         orm_mode=True

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

class User_Update(User_Base):
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
 
class Post_Report_Reason(str, Enum):
    inappropriate = "inappropriate"
    fraudulent = "fraudulent"
    inaccurate = "inaccurate"

class Post_Report(BaseModel):
    post_id: int
    user_id: int
    report_reason: Post_Report_Reason
    user:User
    class Config:
        orm_mode = True
       

class Post_Tag(BaseModel):
    tag:str=Field(...,max_length=20)
    post_id:int=Field(...)
    class Config:
        orm_mode=True

class Post_Comment_Base(BaseModel):
    content: str|None = Field(None, max_length=500, description="Content of the comment")
    

class Post_Comment_Create(Post_Comment_Base):
    pass

class Post_Comment_Update(Post_Comment_Base):
    pass

class Post_Comment(Post_Comment_Base):
    comment_id: int = Field(..., description="Unique ID of the comment")
    commenter: User_Out
    commenter_id: int
    post_id: int
    created_at: int
    image:Image|None
    commenter_id:User
    class Config:
        orm_mode = True

class Post_Base(BaseModel):
    title:str=Field(...,max_length=100)
    post_content:str|None=Field(None,max_length=1000)
    volunteers_needed:int|None=Field(None,gt=0)
    disaster_id:int|None=Field(None)
    
class Post_Create(Post_Base):
    pass

class Post_Update(Post_Base):
    pass

class Post_Enlistment(BaseModel):
    post_id:int
    user:User_Out
    
    class Config:
        orm_mode=True

class Post(Post_Base):
    post_id:int=Field(...)
    creation_time:int=Field(...)
    tags:list[Post_Tag]=Field(...)
    images:list[Image]=Field(...)
    creator:User_Out=Field(...)
    enlistments:list[Post_Enlistment]
    # comments:list[Post_Comment]
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
    disaster_id: int|None=Field(None)

    
        
class Missing_Person_Create(Missing_Person_Base):
    pass

class Missing_Person_Update(Missing_Person_Base):
    pass

class Missing_Person(Missing_Person_Base):
    missing_person_id: int
    creator:User_Out
    creation_time: int
    images:list[Image]=Field(...)
    
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
    #sender_id: int = Field(..., description="ID of the message sender")
    conversation_id: int = Field(..., description="ID of the conversation")
    sent_at:int
    sender:User_Out
    class Config:
        orm_mode = True 

    

class Conversation_Participant(BaseModel):
    #participant_id: int = Field(..., description="Unique ID of the participant entry")
    conversation_id: int = Field(..., description="ID of the conversation")
    is_creator:bool
    
    participant:User_Out
    class Config:
        orm_mode = True
 
        
class Conversation_Base(BaseModel):
    title: str | None = Field(None, max_length=100, description="Title of the conversation")

class Conversation_Create(Conversation_Base):
    pass

class Conversation_Update(Conversation_Base):
    pass

class Conversation(Conversation_Create):
    conversation_id: int = Field(..., description="Unique ID of the conversation")
    is_group: bool = Field(..., description="Whether the conversation is a group conversation")
    created_at: int = Field(..., description="Timestamp of conversation creation")
    messages:list[Message] = Field(...)
    participants:list[Conversation_Participant]
    class Config:
        orm_mode = True

class Post_Comment_Base(BaseModel):
    content: str|None = Field(None, max_length=500, description="Content of the comment")
    

class Post_Comment_Create(Post_Comment_Base):
    pass

class Post_Comment_Update(Post_Comment_Base):
    pass

class Post_Comment(Post_Comment_Base):
    comment_id: int = Field(..., description="Unique ID of the comment")
    commenter: User_Out
    commenter_id: int
    post_id: int
    created_at: int
    image:Image|None
    commenter:User
    class Config:
        orm_mode = True


# Weather models

class Us_Epa_Index(str,Enum):
    Good = "Good"
    Moderate = "Moderate"
    Unhealthy_Sensitive = "Unhealthy for sensitive group"
    Unhealthy = "Unhealthy"
    Very_Unhealthy="Very Unhealthy"
    Hazardous = "Hazardous"



class Location(BaseModel):
    name:str
    country:str
    localtime_epoch:int # in seconds
    localtime:str

class Air_Quality(BaseModel):
    co:float
    o3:float
    no2:float
    so2:float
    pm2_5:float
    pm10:float
    us_epa_index:Us_Epa_Index
    

class Weather_Condition(BaseModel):
    icon:str
    text:str

class Weather(BaseModel):
    temp_c:float
    condition:Weather_Condition
    humidity:int
    feelslike_c:float
    wind_kph:float
    pressure_mb:float
    is_day:int
    air_quality:Air_Quality
    location:Location

class Service_Type(str,Enum):
    shelter="shelter"
    police="police"
    firestation="firestation"
    medical="medical"

class Service_Base(BaseModel):
    service_type:Service_Type
    title:str=Field(...,max_length=100)
    latitude:float
    longitude:float
    details:str|None=Field(None,max_length=500)
    contact_info:str|None=Field(None,max_length=500)

class Service_Create(Service_Base):
    pass

class Service_Update(Service_Base):
    pass

class Service(Service_Base):
    service_id:int
    
    class Config:
        orm_mode=True    
    
    
