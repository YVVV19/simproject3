from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field


class Tournament(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None) 
    name: str
    description: str
    reward: str
    rules: str


    teams: List["Team"] = Relationship(back_populates="tournament")