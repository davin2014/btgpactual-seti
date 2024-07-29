from bson import  ObjectId
from typing import Optional
from pymongo.errors import  PyMongoError
from app.models.customer import CustomerCreate, CustomerUpdate, Customer
from app.db.db import customer_collection


async def get_customers() -> list[Customer]:
    try:
        customers = await customer_collection.find().to_list(1000)
        return customers
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving customers: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving customers: {str(e)}")
    
async def get_customer_by_id(customer_id: str) -> Optional[Customer]:
    try:
        customer_data = await customer_collection.find_one({"_id": ObjectId(customer_id)})
        if customer_data:
            return customer_data
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving customer with id '{customer_id}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving customer with id '{customer_id}': {str(e)}")

async def get_customer_by_name(name: str) -> Optional[Customer]:
    try:
        customer_data = await customer_collection.find_one({"name": name})
        if customer_data:
            return customer_data
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving customer with name '{name}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving customer with name '{name}': {str(e)}")

async def create_customer(customer_data: CustomerCreate) -> Customer:
    try:
        customer_data = customer_data.model_dump(by_alias=True, exclude=["id"])
        result = await customer_collection.insert_one(customer_data)
        if result.inserted_id:
            created_customer = await customer_collection.find_one({"_id": result.inserted_id})
            return Customer(**created_customer)
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error creating customer: {str(e)}")

async def update_customer(customer_id: str, customer_update: CustomerUpdate) -> Optional[Customer]:
    try:
        existing_customer = await customer_collection.find_one({"_id": ObjectId(customer_id)})
        if not existing_customer:
            raise ValueError("Customer not found.")

        update_data = customer_update.model_dump(exclude_unset=True)

        result = await customer_collection.update_one({"_id": ObjectId(customer_id)}, {"$set": update_data})
        if result.modified_count == 1:
            updated_customer_data = await customer_collection.find_one({"_id": ObjectId(customer_id)})
            return Customer(**updated_customer_data)
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error updating customer: {str(e)}")

async def delete_customer(customer_id: str) -> Optional[Customer]:
    try:
        existing_customer = await customer_collection.find_one({"_id": ObjectId(customer_id)})
        if not existing_customer:
            raise ValueError("Customer not found.")

        await customer_collection.delete_one({"_id": ObjectId(customer_id)})
        return existing_customer
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error deleting customer: {str(e)}")