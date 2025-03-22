from fastapi import HTTPException, status, Depends
from sqlmodel import select

from . import Config, User, role_checker, oauth2_scheme
from ..main import app


@app.get("/user")
async def get_user(nickname:str):
    with Config.SESSION as session:
        user = session.exec(select(User).where(User.username == nickname)).first()
        if user:
            return {"message": "Користувач знайдений", "user": user}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

@app.post("/user")
async def create_user(user:User):
    with Config.SESSION as session:
        if session.exec(select(User).where(User.username == user.username)).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": "Користувача створено", "user": user}

@app.put("/user")
async def update_user(user:User):
    with Config.SESSION as session:
        if session.exec(select(User).where(User.username == user.username)).first():
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"message": "Користувача оновлено", "user": user}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

@app.delete("/user")
async def delete_user(nickname:str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        user = session.exec(select(User).where(User.username == nickname)).first()
        if user:
            session.delete(user)
            session.commit()
            return {"message": "Користувача видалено", "user": user}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

