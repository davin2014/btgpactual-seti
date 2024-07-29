import motor.motor_asyncio
from app.core.config import settings
from app.utils.logging_config import logger


try:
    logger.info(f"Attempting to connect to MongoDB with connection string: {settings.mongo_connection_string}")
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_string)
    db = client.college
    user_collection = db.get_collection("user")
    customer_collection = db.get_collection("customer")
    fund_collection = db.get_collection("fund")
    transaction_collection = db.get_collection("transaction")
    logger.info("Successfully connected to MongoDB.")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise
