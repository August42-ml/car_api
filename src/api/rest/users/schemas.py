from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool = Field(default=False)
