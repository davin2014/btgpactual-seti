from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]

class Fund(BaseModel):
    id: Optional[PyObjectId] =  Field(alias="_id", default=None)
    name: str
    minimum_amount: float
    category: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Fund",
                "minimum_amount": 1000,
                "category": "Stocks"
            }
        },
    )