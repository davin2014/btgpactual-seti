from fastapi import APIRouter

from app.api.routes import login, users, customer, fund, transaction

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(customer.router, prefix="/customers", tags=["customers"])
api_router.include_router(fund.router, prefix="/funds", tags=["funds"])
api_router.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
