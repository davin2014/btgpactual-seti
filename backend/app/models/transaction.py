from typing import Optional
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Transaction(BaseModel):
    id: Optional[PyObjectId] =  Field(alias="_id", default=None)
    fund_id: str
    customer_id: str
    amount: float
    type: str # 'linking' or 'unlinking'

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "uuid",
                "fund_id": 1,
                "amount": 1000,
                "type": "linking"
            }
        },
    )

class TransactionCreate(BaseModel):
    fund_id: str
    customer_id: str
    amount: float
    type: str  # 'linking' or 'unlinking'

class TransactionUpdate(BaseModel):
    fund_id: str
    customer_id: str
    amount: float
    type: str  # 'linking' or 'unlinking'

class TransactionInDB(Transaction):
    id: PyObjectId