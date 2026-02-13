from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    username: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserNew(BaseModel):
    email: EmailStr
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)


class UserDelete(BaseModel):
    email: EmailStr


class UserResponse(User):
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str
