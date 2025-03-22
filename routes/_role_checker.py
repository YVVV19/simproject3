from jose import jwt
from sqlmodel import select
from fastapi import HTTPException, status

from .ouath2_jwt import SECRET, ALGORITHM
from db import User


async def role_checker(token, session):
    decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    user = session.exec(select(User).where(User.username == decoded.get("sub"))).first()
    if user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You dont have authority")
    return True
