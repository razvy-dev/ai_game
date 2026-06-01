from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    password: str = Field(min_length = 8, max_length = 120)
    email: str = Field(max_length = 120)
    phone: str | None = Field(max_length=20)
    image: str | None
    ip: str | None

class UserEdit(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    description: str = Field(max_length = 250)
    phone: str | None = Field(max_length=20)
    image: str | None

class UserForgotPassword(BaseModel):
    email: str = Field(max_length = 120)

class UserResetPassword(BaseModel):
    password: str = Field(min_length = 8, max_length = 120)

class UserDelete(BaseModel):
    succes: bool

class UserPrivateResponse(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    description: str | None = Field(max_length=250)
    email: str = Field(max_length = 120)
    phone: str | None = Field(max_length=20)
    image: str | None = Field(max_length = 200)

class UserPublicResponse(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    description: str | None = Field(max_length=250)
    phone: str | None = Field(max_length=20)
    image: str | None = Field(max_length = 200)

class Token(BaseModel):
    access_token: str
    token_type: str