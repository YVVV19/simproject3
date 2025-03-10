from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field
from . import User, Tournament, Result

class Team(SQLModel):
    id: Optional[int] = Field(primary_key=True, default=None) 
    name: str = Field(..., lt=10, ge=4)
    descripton: str = Field(..., lt=100)


    users: List[User] = Relationship(back_populates="team")
    tournament: Tournament = Relationship(back_populates="teams")
    result: Result = Relationship(back_populates="team")