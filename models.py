from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,CheckConstraint
from sqlalchemy.orm import relationship

from database import Base


class Dummy(Base):
    __tablename__="dummy"
    id=Column(Integer(),primary_key=True,autoincrement=True)
    title=Column(String(20),unique=True,nullable=False)