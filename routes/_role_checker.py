from jose import jwt
from sqlmodel import select
from fastapi import HTTPException, status

from . import SECRET, ALGORITHM, Config, User


async def role_checker(token, session):
    with Config.SESSION as session:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user = session.exec(select(User).where(User.username == decoded.get("sub"))).first()
        if user.role != "Admin":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You dont have authority")
        elif user.role == "Admin":
            return True