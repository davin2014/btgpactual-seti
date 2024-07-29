from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "camilo@example.com",
                "password": "securepassword123",
            }
        },
    )


class EmailRequest(BaseModel):
    email: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "camilo@example.com"
            }
        },
    )

class PasswordRecoveryRequest(BaseModel):
    token: str
    new_password: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "token": "string",
                "new_password": "string"
            }
        },
    )