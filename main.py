from fastapi import FastAPI
from db import Config


app=FastAPI()
Config.migrate()


from . import routes