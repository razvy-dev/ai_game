from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    password: str = Field(min_length = 8, max_length = 120)
    email: str = Field(max_length = 120)
    image: str | None = None
    ip: str | None = None

class UserEdit(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    description: str = Field(max_length = 250)
    image: str | None

class UserLogin(BaseModel):
    email: str = Field(max_length=120)
    password: str = Field(min_length=8, max_length=120)

class UserForgotPassword(BaseModel):
    email: str = Field(max_length = 120)

class UserResetPassword(BaseModel):
    password: str = Field(min_length = 8, max_length = 120)

class UserDelete(BaseModel):
    succes: bool

class UserPrivateResponse(BaseModel):
    id: str = Field()
    username: str = Field(min_length = 8, max_length = 25)
    description: str | None = Field(max_length=250)
    email: str = Field(max_length = 120)
    image: str | None = Field(max_length = 200)
    token: Token

class UserPublicResponse(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    description: str | None = Field(max_length=250)
    image: str | None = Field(max_length = 200)
