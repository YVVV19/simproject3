from fastapi import HTTPException, status, Depends
from sqlmodel import select

from db import Config, User
from .ouath2_jwt import oauth2_scheme
from ._role_checker import role_checker
from main import app


#Endpoint for getting all users
@app.get("/user/", summary="Get all users", tags="User")
async def exec_user():
    with Config.SESSION as session:
        users = session.exec(select(User)).all()
        if users:
            return {f"All users: {users}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found users")


#Endpoint for getting user by nickname
@app.get("/user-by-nickname/", summary="Get user by nickname", tags="User")
async def exec_user_by_nickname(nickname:str):
    with Config.SESSION as session:
        user = session.exec(select(User).where(User.username == nickname)).first()
        if user:
            return {f"User with nickname {nickname}: {user}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user by nickname")


#Endpoint for creating user
@app.post("/create-user/", summary="Create user", tags="User")
async def create_user(user:User):
    with Config.SESSION as session:
        if session.exec(select(User).where(User.username == user.username)).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        user.role = "USER"
        session.add(user)
        session.commit()
        session.refresh(user)
        return {f"User created: {user}"}


#Endpoint for updating user
@app.put("/update-user/", summary="Update user", tags="User")
async def update_user(user:User):
    with Config.SESSION as session:
        user_data = session.exec(select(User).where(User.username == user.username)).first()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have such user")
        user.role = "USER"
        update_data = user.model_dump(exclude_unset=True)
        user_data.sqlmodel_update(update_data)
        session.commit()
        session.refresh(user_data)
        return {f"User updated: {user_data}"}


#Endpoint for deleting user
@app.delete("/delete-user/", summary="Delete user", tags="User")
async def delete_user(nickname:str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        user = session.exec(select(User).where(User.username == nickname)).first()
        if user:
            session.delete(user)
            session.commit()
            return {f"User with nickname {nickname} deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user by nickname")
