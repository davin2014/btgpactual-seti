from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from app.models.transaction import Transaction

PyObjectId = Annotated[str, BeforeValidator(str)]

class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255)
    surnames: str = Field(..., max_length=255)
    city: str = Field(..., max_length=255)
    balance: float = 0
   

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Camilo",
                "surnames": "Cruz",
                "city": "Bogota",
                "balance": 1000,
                "is_active": True,
                "is_superuser": False,
            }
        },
    )

class CustomerCreate(CustomerBase):
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Camilo",
                "surnames": "Cruz",
                "city": "Bogota",
                "balance": 1000
            }
        },
    )

class CustomerUpdate(CustomerBase):
        
        model_config = ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_schema_extra={
                "example": {
                    "name": "Camilo",
                    "surnames": "Cruz",
                    "city": "Bogota",
                    "balance": 1000
                }
            },
        )

class Customer(CustomerBase):
    id: Optional[PyObjectId] =  Field(alias="_id", default=None)
    
   

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "uuid",
                "name": "Camilo",
                "surnames": "Cruz",
                "city": "Bogota",
                "balance": 1000
            }
        },
    )


class CustomerResponse(BaseModel):
    id: Optional[PyObjectId] =  Field(alias="_id", default=None)
    name: str
    surnames: str
    city: str
    balance: float

    class Config:
        orm_mode = True


        