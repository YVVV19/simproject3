from fastapi import Depends, HTTPException, status
from sqlmodel import select
from typing import List

from db import Config 
from db.models import User, Team
from .ouath2_jwt import oauth2_scheme 
from ._role_checker import role_checker
from main import app


#Endpoint for getting teams
@app.get("/read-team/", summary="Get all teams", tags=["Team"])
async def read_team(token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        data = session.exec(select(Team)).all()
        if not data:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="We dont have any team")
        return data


#Endpoint for creating team
@app.post("/create-team/", summary="Create team", tags=["Team"])
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


#Endpoint for updating team
@app.put("/update-team/", summary="Update team", tags=["Team"])
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


##Endpoint for deleting team
@app.delete("/delete-team/", summary="Delete team", tags=["Team"])
async def delete_team(team:Team, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token)
        session.delete(team)
        session.commit()
        return "Team successfully delete"
