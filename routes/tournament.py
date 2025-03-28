from fastapi import Depends, HTTPException, status
from sqlmodel import select

from db import Config, Tournament
from .ouath2_jwt import oauth2_scheme
from ._role_checker import role_checker
from main import app


#Endpoint for add tournament
@app.post("/add_tournament/", summary="Add tournament", tags=["Tournament"])
async def add_tournament(tournament: Tournament, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        session.add(tournament)
        session.commit()
        session.refresh(tournament)
        return tournament


#Endpoint for getting all tournaments
@app.get("/all-tournament/", summary="Get all tournaments", tags=["Tournament"])
async def read_all_tournament():
    with Config.SESSION as session:
        data = session.exec(select(Tournament)).all()
        if not data:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="We dont have any tournament")
        return data


#Endpoint for getting tournament by name
@app.get("/tournament/", summary="Get tournament", tags=["Tournament"])
async def read_tournament_by_name(tournament_name:str):
    with Config.SESSION as session:
        data = session.exec(select(Tournament).where(Tournament.name == tournament_name)).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="We dont have any tournament")
        return data


#Endpoint for updating tournament
@app.put("/update-tournament/", summary="Update tournament", tags=["Tournament"])
async def update_tournament(tournament_id: str, tournament:Tournament,  token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        tournament_data = session.get(tournament, tournament_id)
        if not tournament_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"We dont have tournament with id:{tournament_id}")
        update_data = tournament.model_dump(exclude_unset=True)
        vars(tournament_data).update(update_data)
        session.commit()
        session.refresh(tournament_data)
        return {"Info was successfully update to :": f"{tournament_data}"}


#Endpoint for deleting tournament
@app.delete("/delete-tournament/", summary="Delete tournament", tags=["Tournament"])
async def delete_tournament(tournament_name:str, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        role_checker(token, session)
        data = session.exec(select(Tournament).where(Tournament.name == tournament_name)).first()
        session.delete(data)
        session.commit()
        return "tournament successfully delete"
