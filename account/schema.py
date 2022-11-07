import email
from typing import Optional
from pydantic import BaseModel, constr, EmailStr


class Account(BaseModel):
    username: constr(min_length=2, max_length=50)
    email: EmailStr
    password: str


class DisplayAccount(BaseModel):
    id: int
    username: str
    email: str
    firstName: Optional[str]
    lastName: Optional[str]

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    id: Optional[int]