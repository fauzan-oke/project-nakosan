from pydantic import BaseModel
from typing import Optional
from enum import Enum
from dataclasses import dataclass


class Role(str,Enum):
    USER = "user"
    MANAGER = "super_admin"
    ADMIN = "admin"

@dataclass
class SignUser:
    fullname: str
    email: str
    role: Role


class NewUser(BaseModel):
    fullname: str
    email: str
    password: str
    role:Role

    class Config:
        orm_mode = True

class ResUser(BaseModel):
    id: int
    fullname: str
    email: str
    # password: str dont return password as a security practice
    role: Role
    date: str
    time: str
 

    class Config:
        orm_mode = True

      

class ResUpdateUser(BaseModel):
    id: int
    fullname: str
    email: str
    password: str
    role: Role
    date: str
    time: str
 

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class NewRecipient(BaseModel):
    phone_number:int
    fullname:str
    company: str
    status:str
    user_id:int
    date:str 
    time: str

    class Config:
        orm_mode = True


class ResRecipient(BaseModel):
    id: int
    phone_number:int
    fullname: str
    company: str
    status:str 

    class Config:
        orm_mode = True  


class DeletionSuccess(BaseModel):
    status: str = "Success"
    message: str = "User deleted successfully."