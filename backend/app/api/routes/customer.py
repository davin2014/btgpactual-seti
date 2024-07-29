from fastapi import APIRouter,  HTTPException, Depends
from typing import List
from app.models.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.crud.customer import get_customer_by_name, create_customer, update_customer, delete_customer, get_customers, get_customer_by_id

router = APIRouter()

@router.get("/customers/", response_model=List[CustomerResponse])
async def read_customers_():
    customers = await get_customers()
    if customers is None:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def read_customer(customer_id: str ):
    customer = await get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer with id '{customer_id}' not found")
    return customer

@router.get("/customers/{name}", response_model=CustomerResponse)
async def read_customer(name: str ):
    customer = await get_customer_by_name(name)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer '{name}' not found")
    return customer

@router.post("/customers/", response_model=CustomerResponse)
async def create_new_customer(customer: CustomerCreate ):
    try:
        new_customer = await create_customer(customer)
        return new_customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_existing_customer(customer_id: str, customer_update: CustomerUpdate ):
    try:
        updated_customer = await update_customer(customer_id, customer_update)
        if updated_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/customers/{customer_id}", response_model=CustomerResponse)
async def delete_existing_customer(customer_id: str ):
    try:
        deleted_customer = await delete_customer(customer_id)
        if deleted_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return deleted_customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))