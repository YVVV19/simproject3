from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator


class Result(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None) 
    score: int

    team_id: int = Field(foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="result")


    @field_validator("score")
    @classmethod
    def score(cls, v):
        if v <= 0:
            raise ValueError("Score cant be below zero")
        return v