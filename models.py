from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey

Base = declarative_base()
##우리가 쓸거
#유저 성별
class Gender(str, Enum):
    male = "male"
    female = "female"

# 유저 역할
class Role(str, Enum): 
    admin = "admin"
    user = "user"
    student = "student"

##우리가 쓸거
class Type(str, Enum):
    user = 'user'
    bot = 'bot'
##우리가 쓸거
# class Part(str, Enum):
#     pic = "picture"
#     talk = 'talk'

class NANDK(str, Enum):
    normal="normal"
    keyword="keyword"

class Keyword(int, Enum):
    pass




class User(BaseModel):
    # Optional : 필수적으로 필요한 것은 아님
    id : Optional[UUID] = uuid4() # UUID : 범용 공유 식별자(Universally unique indentifier)
    first_name : str
    last_name : str
    middle_name : Optional[str]
    gender : Gender # class로 정의되어 있음
    roles : List[Role]

class UserUpdateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    roles: Optional[List[Role]]


##우리가 쓸거
# class Chatting(BaseModel):
#     str: Optional[str]
#     type: Type
#     part: Part
#     time: Optional[datetime] = datetime().now()

class NormalQ(BaseModel):
    num : int
    qqq : str
    # type: 





##################################################진짜 설계
class USER(BaseModel):
    # userid: Optional[UUID] = uuid4()
    userid: int
    name: str
    age: int = 1
    gender: Gender

class USER_TESTDAY(BaseModel):
    # userid: Optional[UUID] = uuid4()
    userid: int
    date: date

class QUESTION(BaseModel):
    type: NANDK
    sentence: str
    keyword: Optional[Keyword]

class TALKREPORT(BaseModel):
    # userid: Optional[UUID] = uuid4()
    userid: int
    date: date
    emo: int = 0
    result: str

class DRAWREPORT(BaseModel):
    # userid: Optional[UUID] = uuid4()
    userid: int
    date: date
    house: Optional[str]
    tree: Optional[str]
    person: Optional[str]
    result: str

class CHATTING(BaseModel):
    # userid: Optional[UUID] = uuid4()
    userid: int
    # date: date
    type: Optional[str]
    chat: Optional[str]

class Sendtext(BaseModel):
    userid : int
    text : str
