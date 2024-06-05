# items.py

from pydantic import BaseModel, Field, field_validator, ValidationError


class LibraryItem(BaseModel):
    is_borrowed: bool = Field(default=False)
    title: str = Field(..., max_length=60)
    isbn: str = Field(Field(..., pattern=r'^\d{9}$'))
