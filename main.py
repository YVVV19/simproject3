from fastapi import FastAPI
from db import Config


app=FastAPI()
Config.migrate()


from routes import websocket, team, tournament, user, ouath2_jwt