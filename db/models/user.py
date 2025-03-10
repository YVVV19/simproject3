from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator, EmailStr
import re


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)    
    username: str
    gamer_nickname: str
    email: EmailStr
    password: str

    
    team: Optional["Team"] = Relationship(back_populates="users")


    @field_validator("username")
    @classmethod
    def name(cls, v):
        if not str(v).isalpha:
            raise ValueError("Name must include only alphabet symbols!!!")
        return v
    

    @field_validator("password")
    @classmethod
    def password(cls,v):
        if not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"):
            raise ValueError("Your password cant go through validation")
        return v