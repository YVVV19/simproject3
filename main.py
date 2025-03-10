from fastapi import FastAPI
from db import Config


app=FastAPI()
Config.migrate()