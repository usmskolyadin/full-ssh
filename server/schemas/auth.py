from pydantic import BaseModel, EmailStr
from typing import Optional


class SUser(BaseModel):
    email: EmailStr
    password: str
    is_avaible: Optional[bool] = None
