import os
import psutil
import json
import random
from typing import List, Dict
import requests
from fastapi import FastAPI
from pydantic import BaseModel
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6

class WorldModel(BaseModel):
    """Pydantic model for FastAPI usage"""
    time: int
    state: List[list]
    scores: Dict[str, int]

app = FastAPI()

@app.get("/")
def read_root():
    return {"name": "random-agent"}

@app.post("/action/")
def get_action(state: WorldModel):
    print("Ram used:", get_ram())
    return {"action": random.randint(1, 4)}

@app.on_event("startup")
def start_agent_server():
    with open("heroku_app_name.txt", 'r') as f:
        HEROKU_APP_NAME = f.read()
    agent_api = f"https://{HEROKU_APP_NAME}.herokuapp.com"
    game = "https://open-worlds.herokuapp.com"
    params = (
        ('agent_api', agent_api),
    )
    response = requests.post(f"{game}/connect/", params=params)
    print(f"Connection {json.loads(response.text)['result']}.")
