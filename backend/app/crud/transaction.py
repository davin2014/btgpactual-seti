from bson import  ObjectId
from typing import List, Optional
from pymongo.errors import  PyMongoError
from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.db.db import transaction_collection
from app.utils.logging_config import logging


async def get_transactions() -> list[Transaction]:
    try:
        transactions = await transaction_collection.find().to_list(1000)
        return transactions
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving transactions: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving transactions: {str(e)}")
    

async def get_transaction_by_id(transaction_id: str) -> Optional[Transaction]:
    try:
        transaction_data = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
        if transaction_data:
            return transaction_data
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving transaction with id '{transaction_id}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving transaction with id '{transaction_id}': {str(e)}")

async def get_transaction_by_fund_id(fund_id: str) -> List[Transaction]:
    try:
        transaction_data = await transaction_collection.find({"fund_id": fund_id})
        if transaction_data:
            return transaction_data
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving transaction with fund id '{fund_id}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving transaction with fund id '{fund_id}': {str(e)}")

async def get_transactions_by_customer_id(customer_id: str) -> List[Transaction]:
    try:
        cursor = transaction_collection.find({"customer_id": customer_id})
        transactions = []
        async for transaction_data in cursor:
            transactions.append(Transaction(**transaction_data))
        return transactions
    except PyMongoError as e:
        raise RuntimeError(f"Database error while retrieving transactions with customer id '{customer_id}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while retrieving transactions with customer id '{customer_id}': {str(e)}")  

async def create_transaction(transaction_data: TransactionCreate) -> Transaction:
    try:
        transaction_data = transaction_data.model_dump(by_alias=True, exclude=["id"])
        result = await transaction_collection.insert_one(transaction_data)
        if result.inserted_id:
            created_transaction = await transaction_collection.find_one({"_id": result.inserted_id})
            return Transaction(**created_transaction)
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error creating transaction: {str(e)}")
    

async def update_transaction(transaction_id: str, transaction_update: TransactionUpdate) -> Transaction:
    try:
        logging.info(f"Updating transaction with ID: {transaction_id}")
        existing_transaction = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
        if not existing_transaction:
            logging.warning(f"Transaction with ID {transaction_id} not found.")
            raise ValueError("Transaction not found.")

        update_data = transaction_update.model_dump(exclude_unset=True)
        logging.info(f"Update data: {update_data}")

        result = await transaction_collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})
        if result.modified_count == 1:
            updated_transaction = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
            logging.info(f"Updated transaction: {updated_transaction}")
            return Transaction(**updated_transaction)
        logging.info(f"No modifications made to the transaction with ID {transaction_id}.")
        return None
    except PyMongoError as e:
        logging.error(f"Database error: {str(e)}")
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating transaction: {str(e)}")
        raise RuntimeError(f"Error updating transaction: {str(e)}")
    

async def delete_transaction(transaction_id: str) -> Optional[Transaction]:
    try:
        deleted_transaction = await transaction_collection.find_one_and_delete({"_id": ObjectId(transaction_id)})
        if deleted_transaction:
            return deleted_transaction
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Database error while deleting transaction with id '{transaction_id}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while deleting transaction with id '{transaction_id}': {str(e)}")


