import re
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from typing import ClassVar

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    password: str = Field(min_length = 8, max_length = 120)
    email: EmailStr
    image: str | None = None
    ip: str | None = None

    @classmethod
    def sanitize_username(cls, v: str) -> str:
        return re.sub(r'[^\w\s]', '', v).strip().lower()

    @classmethod
    def sanitize_ip(cls, v: str) -> str:
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        if re.match(ipv4_pattern, v) or re.match(ipv6_pattern, v):
            return v
        raise ValueError(f"Invalid IP address: {v}")

    @field_validator('username')
    @classmethod
    def validate_and_sanitize_username(cls, v: str) -> str:
        sanitized = cls.sanitize_username(v)
        if not re.match(r'^[a-z0-9_]+$', sanitized):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        if len(sanitized) < 3:
            raise ValueError("Username must be at least 3 characters after sanitization")
        return sanitized

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator('ip')
    @classmethod
    def validate_and_sanitize_ip(cls, v: str) -> str | None:
        if v is None:
            return None
        if not v.strip():
            return None
        return cls.sanitize_ip(v)

class UserEdit(BaseModel):
    username: str = Field(min_length = 8, max_length = 25)
    description: str = Field(max_length = 250)
    image: str | None

    @field_validator('username')
    @classmethod
    def validate_and_sanitize_username(cls, v: str) -> str:
        sanitized = cls.sanitize_username(v)
        if not re.match(r'^[a-z0-9_]+$', sanitized):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        if len(sanitized) < 3:
            raise ValueError("Username must be at least 3 characters after sanitization")
        return sanitized

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=120)

class UserForgotPassword(BaseModel):
    email: EmailStr

class UserResetPassword(BaseModel):
    password: str = Field(min_length = 8, max_length = 120)
    token: str | None = None
    currentPassword: str | None = None
    user_id: str | None = None

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v

    @model_validator(mode='after')
    def validate_currentPassword_or_token(self):
        if not self.token and not self.currentPassword:
            raise ValueError("You need to provide either the current password or a token to be able to access this.")
        if self.token and self.currentPassword:
            raise ValueError("You cannot provide both a token and a current password.")
        if self.currentPassword and not self.user_id:
            raise ValueError("user_id is required when using currentPassword.")
        return self

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
