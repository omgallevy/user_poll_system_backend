from datetime import date
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    age: int
    address: str
    joining_date: Optional[date]
    is_registered: Optional[bool] = False
