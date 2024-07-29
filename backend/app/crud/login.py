from app.models.user import User
from typing import Optional
from app.core.security import  verify_password
from app.crud.user import get_user_by_email
from app.db.db import db
from app.utils.logging_config import logger



async def authenticate(email: str, password: str) -> Optional[User]:
    try:
        if not email or not password:
            raise ValueError("Email and password must be provided")
        
        logger.info(f"Authenticating user with email: {email}")
        db_user = await get_user_by_email(email=email)
        if not db_user:
            logger.error(f"No user found with email: {email}")
            return None
        
        if not verify_password(password, db_user.hashed_password):
            logger.error(f"Password verification failed for user: {email}")
            return None
        
        logger.info(f"User authenticated successfully: {email}")
        return db_user
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return None
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return None