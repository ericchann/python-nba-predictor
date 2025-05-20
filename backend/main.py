from fastapi import FastAPI
from pydantic import BaseModel
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd

app = FastAPI()

class PropRequest(BaseModel):
    player_name: str
    stat: str  # e.g., "points"

@app.post("/predict")
def predict_prop(req: PropRequest):
    player = players.find_players_by_full_name(req.player_name)[0]
    gamelog = playergamelog.PlayerGameLog(player_id=player['id'], season='2024-25')
    df = gamelog.get_data_frames()[0]
    df = df.sort_values("GAME_DATE").tail(10)
    avg = df[req.stat.upper()].mean()
    return {"prediction": round(avg, 1)}
