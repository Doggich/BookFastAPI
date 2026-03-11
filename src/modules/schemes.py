from enum import Enum
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class BookFormatScheme(str, Enum):     
    HARDCOVER = "Hardcover"
    PAPERBACK = "Paperback"
    EBOOK = "E-book"

class BookMetaDataScheme(BaseModel):
    pages: int = Field(gt=0)         
    format_: BookFormatScheme = Field(alias="format")        

class BookScheme(BaseModel):
    title: str = Field(max_length=100)
    author: str = Field(max_length=50)
    year: int = Field(gt=0)
    genre: list[str] = Field(min_length=1)  
    is_available: bool
    metadata: BookMetaDataScheme

    @field_validator('year')
    @classmethod
    def year_not_in_future(cls, v: int):
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(f'The year cannot be in the future (it is {current_year})!')
        return v