import asyncio
from app.models.user import UserCreate
from app.crud.user import create_user, get_user_by_email
from app.models.fund import Fund
from app.crud.fund import create_fund

async def create_test_user():
    try:
        email = "testuser@example.com"
        existing_user = await get_user_by_email(email=email)
        if existing_user:
            print(f"A user with email {email} already exists.")
            return
        
        user_in = UserCreate(
            email=email,
            password="testpassword",
            name="Test",
            surnames="User"
        )
        user = await create_user(user=user_in)
        print(f"Test user created: {user.email}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def create_fund_records():
    funds = [
        Fund(consecutive=1, name="FPV_BTG_PACTUAL_RECAUDADORA", minimum_amount=75000, category="FPV"),
        Fund(consecutive=2, name="FPV_BTG_PACTUAL_ECOPETROL", minimum_amount=125000, category="FPV"),
        Fund(consecutive=3, name="DEUDAPRIVADA", minimum_amount=50000, category="FIC"),
        Fund(consecutive=4, name="FDO-ACCIONES", minimum_amount=250000, category="FIC"),
        Fund(consecutive=5, name="FPV_BTG_PACTUAL_DINAMICA", minimum_amount=100000, category="FPV")
    ]
    
    for fund in funds:
        try:
            created_fund = await create_fund(fund_data=fund)
            print(f"Created fund: {created_fund.name}")
        except Exception as e:
            print(f"An error occurred while creating fund {fund.name}: {e}")

async def main():
    await create_test_user()
    await create_fund_records()

if __name__ == "__main__":
    asyncio.run(main())