from fastapi import Depends, HTTPException, status
from sqlmodel import select
from typing import List

from . import Config, User, Team, oauth2_scheme, role_checker
from ..main import app


@app.get("/read-team/")
async def read_team(token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        data = session.exec(select(Team)).all()
        if not data:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="We dont have any team")
        return data
    

@app.post("/create-team/")
async def create_team(team:Team, user_uucs: List[str], token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token)
        val = session.exec(select(Team).where(Team.name == team.name)).first()
        if val:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="We already have team with this name")
        players = session.exec(select(User).where(User.uuc.in_(user_uucs))).all()
        if not players:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No uuc was capture")
        team_data = Team(name=team.name, descripton=team.descripton, users=players)
        session.add(team_data)
        session.commit()
        session.refresh(team_data)
        return team_data
    

@app.put("/update-team/")
async def update_team(team_id: str, team:Team,  token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token)
        team_data = session.get(Team, team_id)
        if not team_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have team with id:{team_id}") 
        update_data = team.model_dump(exclude_unset=True)
        vars(team_data).update(update_data)
        session.commit()
        session.refresh(team_data)
        return {"Info was successfully update to :": f"{team_data}"}
    

@app.delete("/delete-team/")
async def delete_team(team:Team, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token)
        session.delete(team)
        session.commit()
        return "Team successfully delete"