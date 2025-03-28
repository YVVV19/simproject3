from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field

class Team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None) 
    name: str = Field(..., lt=10, ge=4)


    users: List["User"] = Relationship(back_populates="team")
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")
    tournament: Optional["Tournament"] = Relationship(back_populates="teams")
    result: Optional["Result"] = Relationship(back_populates="team")
    