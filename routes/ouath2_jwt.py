from os import getenv
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from jose import jwt, JWTError
from datetime import datetime, timedelta

from . import Config, User, Tournament
from ..main import app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()

SECRET = getenv("SECRET_TOKEN")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = getenv("TOKEN_EXPIRE")


@app.post("/token/")
async def token(form: OAuth2PasswordRequestForm = Depends()):
    with Config.SESSION as session:
        user = session.exec(select(User).where(User.username == form.username)).first()
        if user:
            try:
                decoded = jwt.decode(user.password, SECRET, algorithms=[ALGORITHM])["password"]
                if decoded == form.password:
                    access_token = jwt.encode({"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)}, SECRET, algorithm=ALGORITHM)
                    return{
                        "access_token": access_token,
                        "token_type": "bearer",
                        }
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authority")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authority")


@app.post("/registration")
async def regist_user(user:User):
    jwt_token = jwt.encode({"password": user.password}, SECRET, algorithm=ALGORITHM)
    user.password = jwt_token

    with Config.SESSION as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    

@app.get("/add_tournament")
async def add_tournament(tournament: Tournament, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user = session.exec(select(User).where(User.username == decoded.get("sub"))).first()
        if user.role == "Admin":
            session.add(tournament)
            session.commit()
            session.refresh(tournament)
            return tournament