from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(max_length=20)
    birthday: date = Field(description="Дата в форматі 'YYYY-MM-DD'")
    other_data: Optional[str] = Field(max_length=20)


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    other_data: str = 'Other data'
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

