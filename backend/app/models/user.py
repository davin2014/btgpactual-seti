import uuid
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from app.models.transaction import Transaction

from typing import List, Optional

# Shared properties
class UserBase(BaseModel):
    """
    Shared properties of all users
    """
    email: EmailStr = Field(..., max_length=255)
    name: str = Field(..., max_length=255)
    surnames: str = Field(..., max_length=255)
    is_active: bool = True
    is_superuser: bool = False

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "camilo@example.com",
                "name": "Camilo",
                "surnames": "Cruz",
                "is_active": True,
                "is_superuser": False,
            }
        },  
        )
    

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "camilo@example.com",
                "name": "Camilo",
                "surnames": "Cruz",
                "password": "securepassword123",
            }
        },  
        )

class UserRegister(UserBase):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=40)
    name: str = Field(..., max_length=255)
    surnames: str = Field(..., max_length=255)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "camilo@example.com",
                "name": "Camilo",
                "surnames": "Cruz",
                "password": "securepassword123",
            }
        },
    )


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, max_length=255)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "camilo@example.com",
                "name": "Camilo",
                "surnames": "Cruz",
                "is_active": True,
                "is_superuser": False,
            }
        },
    )

class UserUpdateMe(UserBase):
    name: str = Field(..., max_length=255)
    surnames: str = Field(..., max_length=255)
    city: str = Field(..., max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=255)

class UserInDB(UserBase):
    hashed_password: str


class UpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=40)
    new_password: str = Field(..., min_length=8, max_length=40)

# Database model
class User(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(..., max_length=255)
    surnames: str = Field(..., max_length=255)
    hashed_password: str
    




class UserPublic(UserBase):
    id: uuid.UUID

# Generic message
class Message(BaseModel):
    message: str

# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(BaseModel):
    sub: Optional[str] = None

class NewPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=40)