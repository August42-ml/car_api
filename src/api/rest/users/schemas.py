from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool = Field(default=False)
