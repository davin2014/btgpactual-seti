from fastapi import APIRouter,  HTTPException, Depends
from typing import List
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.fund import Fund
from app.crud.fund import get_funds, get_fund_by_id, create_fund, update_fund, delete_fund

router = APIRouter()


@router.get("/", response_model=List[Fund])
async def read_funds():
    return await get_funds()

@router.get("/{fund_id}", response_model=Fund)
async def read_fund(fund_id: str):
    fund = await get_fund_by_id(fund_id)
    if fund:
        return fund
    raise HTTPException(status_code=404, detail="Fund not found")



@router.post("/funds/", response_model=Fund)
async def create_fund_(fund: Fund):
    fund = await create_fund(fund)
    if fund:
        return fund
    else:
        raise HTTPException(status_code=400, detail="Fund not created")

@router.put("/{fund_id}", response_model=Fund)
async def update_fund_(fund_id: str, fund: Fund):
    updated_fund = await update_fund(fund_id, fund)
    if updated_fund:
        return updated_fund
    raise HTTPException(status_code=404, detail="Fund not found")

@router.delete("/{fund_id}", response_model=Fund)
async def delete_fund_(fund_id: str):
    deleted_fund = await delete_fund(fund_id)
    if deleted_fund:
        return deleted_fund
    raise HTTPException(status_code=404, detail="Fund not found")
