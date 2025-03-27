from fastapi import Depends, HTTPException, status
from sqlmodel import select

from db import Config, Result, Team
from .ouath2_jwt import oauth2_scheme
from ._role_checker import role_checker
from main import app


@app.get("get-result-by-team-name")
async def get_result_by_name(team_name:str):
    with Config.SESSION as session:
        data = session.exec(select(Team).where(Team.name == team_name)).first()
        return data


@app.put("/update-score/")
async def update_score(team_name: str, score:Result, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        data = session.exec(select(Team).where(Team.name == team_name)).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have team with id:{team_name}")
        update_data = data(result=score)
        data.sqlmodel_update(update_data)
        session.commit()
        session.refresh(data)
        return {"Info was successfully update"}

@app.delete("/delete-score/")
async def delete_score(team_name:str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        data = session.exec(select(Team).where(Team.name == team_name)).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have team with id:{team_name}")
        update_data = data(result=0)
        data.sqlmodel_update(update_data)
        session.commit()
        session.refresh(data)