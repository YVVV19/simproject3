from typing import Optional, List
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator
from . import Team


class Result(SQLModel):
    id: Optional[int] = Field(primary_key=True, default=None) 
    score: int


    team: Team = Relationship(back_populates="result")


    @field_validator("score")
    @classmethod
    def score(cls, v):
        if v <= 0:
            raise ValueError("Score cant be below zero")
        return v