from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    firstname: str = Field(max_length=50)
    secondname: str = Field(max_length=50)
    email: str = Field(max_length=50)
    telephone: int 
    birthday: date 

   
class ContactNotes(ContactBase):
    notes: str | None = None


class ContactResponse(ContactBase):
    notes: str | None

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    
class RequestEmail(BaseModel):
    email: EmailStr    
    
