from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    
    sender_id: int = Field(foreign_key="user.id")
    sender: Optional["User"] = Relationship(back_populates="messages")