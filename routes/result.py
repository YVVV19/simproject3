from fastapi import Depends, HTTPException, status
from sqlmodel import select
from typing import List

from db import Config, User, Tournament, Result, Team
from .ouath2_jwt import oauth2_scheme
from ._role_checker import role_checker
from main import app


@app.get("get-result-by-team-name")
async def get_result_by_name(team_name:str):
    with Config.SESSION as session:
        data = session.exec(select(Team).where(Team.name == team_name)).first()
        return data


@app.put("/update-team/")
async def update_team(team_name: str, score:Result, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        data = session.exec(select(Team).where(Team.name == team_name)).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have team with id:{team_name}")
        update_data = data(result=score)
        vars(data).update(update_data)
        session.commit()
        session.refresh(data)
    

@app.delete("/delete-team/")
async def delete_team(team_name:str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        data = session.exec(select(Team).where(Team.name == team_name)).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have team with id:{team_name}")
        update_data = data(result=0)
        vars(data).update(update_data)
        session.commit()
        session.refresh(data)