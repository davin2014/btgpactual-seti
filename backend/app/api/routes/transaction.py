from fastapi import APIRouter,  HTTPException, Depends
from typing import List
from app.models.transaction import TransactionCreate, TransactionUpdate, Transaction
from app.crud.transaction import get_transactions, get_transaction_by_id, get_transaction_by_fund_id, get_transactions_by_customer_id, create_transaction, update_transaction, delete_transaction
router = APIRouter()


@router.get("/transactions/", response_model=List[Transaction])
async def read_transactions_():
    transactions = await get_transactions()
    if transactions is None:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def read_transaction(transaction_id: str ):
    transaction = await get_transaction_by_id(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail=f"Transaction with id '{transaction_id}' not found")
    return transaction

@router.get("/transactions/fund/{fund_id}", response_model=List[Transaction])
async def read_transaction(fund_id: str ):
    transaction = await get_transaction_by_fund_id(fund_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail=f"Transaction with fund id '{fund_id}' not found")
    return transaction

@router.get("/transactions/customer/{customer_id}", response_model=List[Transaction])
async def read_transaction(customer_id: str ):
    transaction = await get_transactions_by_customer_id(customer_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail=f"Transaction with customer id '{customer_id}' not found")
    return transaction

@router.post("/transactions/", response_model=Transaction)
async def create_new_transaction(transaction: TransactionCreate ):
    try:
        new_transaction = await create_transaction(transaction)
        return new_transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_existing_transaction(transaction_id: str, transaction_update: TransactionUpdate ):
    try:
        updated_transaction = await update_transaction(transaction_id, transaction_update)
        if updated_transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return updated_transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/transactions/{transaction_id}", response_model=Transaction)
async def delete_existing_transaction(transaction_id: str ):
    try:
        deleted_transaction = await delete_transaction(transaction_id)
        if deleted_transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return deleted_transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


