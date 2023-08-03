from sqlalchemy import String,Boolean,Integer,Column,Text, Enum
from database.database import Base
from schema.schema import Role

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    fullname=Column(String(255),nullable=False)
    email=Column(Text,nullable=False,unique=True)
    password=Column(String(255),nullable=False)
    date=Column(String(255),nullable=False)
    time=Column(String(244),nullable=False)
    role=Column(Enum(Role))

class RecipientList(Base):
    __tablename__='recipient_list'
    id=Column(Integer,primary_key=True)
    phone_number=Column(Integer,nullable=False)
    fullname=Column(String(255),nullable=False)
    company=Column(String(255),nullable=False)    
    status=Column(String(255),nullable=False)
    user_id=Column(Integer,nullable=False)
    date=Column(String(255),nullable=False)
    time=Column(String(244),nullable=False)