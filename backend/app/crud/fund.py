
from bson import  ObjectId
from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import  PyMongoError
from app.models.fund import Fund
from app.db.db import fund_collection




async def get_funds() -> List[Fund]:
    try:
        funds = await fund_collection.find().to_list(1000)
        return funds
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving funds: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving funds: {str(e)}")
    

async def get_fund_by_id(fund_id: str) -> Optional[Fund]:
    try:
        fund = await fund_collection.find_one({"_id": ObjectId(fund_id)})
        if fund:
            return fund
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving fund with id '{fund_id}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving fund with id '{fund_id}': {str(e)}")
    

async def create_fund(fund_data: Fund) -> Fund:
    try:
        fund_data = fund_data.model_dump(by_alias=True, exclude=["id"])
        result = await fund_collection.insert_one(fund_data)
        if result.inserted_id:
            created_fund = await fund_collection.find_one({"_id": result.inserted_id})
            if created_fund:
                created_fund["id"] = str(created_fund.pop("_id"))
                return Fund(**created_fund)
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except ValidationError as e:
        raise RuntimeError(f"Validation error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error creating fund: {str(e)}")
    
async def update_fund(fund_id: str, fund_data: Fund) -> Optional[Fund]:
    try:
        existing_fund = await fund_collection.find_one({"_id": ObjectId(fund_id)})
        if not existing_fund:
            raise ValueError("Fund not found.")
        
        update_data = fund_data.model_dump(exclude_unset=True)
        
        result = await fund_collection.update_one({"_id": ObjectId(fund_id)}, {"$set": update_data})
        if result.modified_count == 1:
            updated_fund_data = await fund_collection.find_one({"_id": ObjectId(fund_id)})
            return Fund(**updated_fund_data)
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error updating fund: {str(e)}")
    

async def delete_fund(fund_id: str) -> Optional[Fund]:
    try:
        existing_fund = await fund_collection.find_one({"_id": ObjectId(fund_id)})
        if not existing_fund:
            raise ValueError("Fund not found.")
        
        delete_result = await fund_collection.delete_one({"_id": ObjectId(fund_id)})
        if delete_result.deleted_count == 1:
            existing_fund["id"] = str(existing_fund.pop("_id"))
        
        return existing_fund
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error deleting fund: {str(e)}")