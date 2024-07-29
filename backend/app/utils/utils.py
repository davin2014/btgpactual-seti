import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import os
from jinja2 import Environment, FileSystemLoader
from app.utils.logging_config import logger


import emails  # type: ignore
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError

from app.core.config import settings


@dataclass
class EmailData:
    html_content: str
    subject: str


import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def render_email_template(template_name: str, context: dict) -> str:
    """
    Render an email template with the given context.

    Args:
        template_name (str): The name of the template file.
        context (dict): The context to render the template with.

    Returns:
        str: The rendered template as a string.
    """
    try:
       
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'email-templates/build/')
        print(f"Template directory: {template_dir}")
        
        
        if not os.path.isdir(template_dir):
            raise RuntimeError(f"Template directory '{template_dir}' does not exist")
        
        
        template_path = os.path.join(template_dir, template_name)
        print(f"Template path: {template_path}")    
        if not os.path.isfile(template_path):
            raise RuntimeError(f"Template '{template_name}' not found in directory '{template_dir}'")
        
        
        env = Environment(loader=FileSystemLoader(template_dir))
        
        template = env.get_template(template_name)
        print(f"Loaded template: {template_name}")
        
        
        return template.render(context)
    except TemplateNotFound:
        raise RuntimeError(f"Template '{template_name}' not found in directory '{template_dir}'")
    except Exception as e:
        print(f"Error: {e}")
        raise RuntimeError(f"Error rendering template '{template_name}': {str(e)}")


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"

    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )

    smtp_options = {
        "host": settings.SMTP_HOST, 
        "port": settings.SMTP_PORT
    }

    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True

    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    response = message.send(to=email_to, smtp=smtp_options)
    
    logging.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    try:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Password recovery for user {email}"
        link = f"{settings.server_host}/reset-password?token={token}"
        html_content = render_email_template(
            template_name="reset_password.html",
            context={
                "project_name": settings.PROJECT_NAME,
                "username": email,
                "email": email_to,
                "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
                "link": link,
            },
        )
        return EmailData(html_content=html_content, subject=subject)
    except RuntimeError as e:
        print(f"Failed to generate reset password email: {e}")
        raise


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except InvalidTokenError as e:
        logger.error(f"Invalid token error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None