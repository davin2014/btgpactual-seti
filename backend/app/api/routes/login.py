from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.crud.login import authenticate
from app.crud.user import get_user_by_email, update_password
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import Message, NewPassword, Token, UserPublic
from app.models.login import LoginRequest, EmailRequest, PasswordRecoveryRequest
from app.utils.utils import generate_password_reset_token, generate_reset_password_email, send_email, verify_password_reset_token
from app.utils.logging_config import logger

router = APIRouter()

@router.post("/login/access-token")
async def login_access_token(
     form_data: LoginRequest
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info("Received login request")
    try:
        user = await authenticate(
             email=form_data.username, 
             password=form_data.password
        )
		
        if not user:
            logger.error("Authentication failed: Incorrect email or password")
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        elif not user.is_active:
            logger.error("Authentication failed: Inactive user")
            raise HTTPException(status_code=400, detail="Inactive user")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = Token(
            access_token=security.create_access_token(
                user.id, expires_delta=access_token_expires
            )
        )
        logger.info("Token created successfully")
        return token
    except HTTPException as e:
        # Re-raise HTTPExceptions to avoid catching them in the general exception handler
        raise e
    except Exception as e:
        logger.exception("An error occurred during login")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
	"""
	Test access token
	"""
	return current_user


@router.post("/password-recovery", response_model=Message)
def recover_password(email_request: EmailRequest) -> Message:
    """
    Endpoint to handle password recovery requests.
    
    Args:
        email_request (EmailRequest): The email address of the user requesting password recovery.
    
    Returns:
        Message: A message indicating the result of the password recovery request.
    """
    email = email_request.email

    # Log the email received
    logger.info(f"Received password recovery request for email: {email}")

    # Retrieve the user by email
    user = get_user_by_email(email=email)
    logger.info(f"User found: {user}")

    # Log the result of the user retrieval
    if user:
        logger.info(f"User found: {user}")
    else:
        logger.info("User not found")

    # If the user does not exist, raise a 404 error
    if not user:
        logger.exception(f"User not found: {email}")
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )


    # Generate a password reset token for the user
    password_reset_token = generate_password_reset_token(email=email)

    # Generate the email content for the password reset
    email_data = generate_reset_password_email(
        email_to=email, email=email, token=password_reset_token
    )

    # Send the password reset email
    send_email(
        email_to=email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )

    # Return a success message
    return Message(message="Password recovery email sent")



@router.post("/reset-password/")
async def reset_password(request: PasswordRecoveryRequest) -> Message:
    """
    Reset password
    """
    try:
        email = verify_password_reset_token(token=request.token)
        logger.info(f"Email found: {email}")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = get_user_by_email(email=email)
        logger.info(f"User found: {user}")
        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this email does not exist in the system.",
            )
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        user = await update_password(user_id=user.id, password=request.new_password)
        if user:
            return Message(message="Password updated successfully")
        else:
            raise HTTPException(status_code=404, detail="User not found or password not updated")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
     

@router.post(
	"/password-recovery-html-content/{email}",
	dependencies=[Depends(get_current_active_superuser)],
	response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
	"""
	HTML Content for Password Recovery
	"""
	user = get_user_by_email(session=session, email=email)

	if not user:
		raise HTTPException(
			status_code=404,
			detail="The user with this username does not exist in the system.",
		)
	password_reset_token = generate_password_reset_token(email=email)
	email_data = generate_reset_password_email(
		email_to=user.email, email=email, token=password_reset_token
	)

	return HTMLResponse(
		content=email_data.html_content, headers={"subject:": email_data.subject}
	)