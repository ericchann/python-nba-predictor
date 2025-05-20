from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
from requests.exceptions import ReadTimeout

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your React app's domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class PropRequest(BaseModel):
    player_name: str
    stat: str  # e.g., "points"

@app.get("/")
def read_root():
    return {"message": "Welcome to the NBA Predictor API!"}

@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}

@app.post("/predict")
def predict_prop(req: PropRequest):
    try:
        player = players.find_players_by_full_name(req.player_name)[0]
        gamelog = playergamelog.PlayerGameLog(player_id=player['id'], season='2024-25')
        df = gamelog.get_data_frames()[0]
        df = df.sort_values("GAME_DATE").tail(10)
        avg = df[req.stat.upper()].mean()
        return {"prediction": round(avg, 1)}
    except ReadTimeout:
        return {"error": "The request to stats.nba.com timed out. Please try again later."}
    except IndexError:
        return {"error": "Player not found. Please check the player name and try again."}
