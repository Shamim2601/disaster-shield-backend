from typing import Annotated

from pydantic import BaseModel,Field
from enum import Enum

class Dummy(BaseModel):
    id:int
    title:str=Field(...,max_length=20)
    class Config:
        orm_mode=True