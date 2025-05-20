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

STAT_MAPPING = {
    "points": "PTS",
    "rebounds": "REB",
    "assists": "AST",
    "steals": "STL",
    "blocks": "BLK",
    "turnovers": "TOV",
    "fouls": "PF",
    "plus_minus": "PLUS_MINUS",
    # Add more mappings as needed
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the NBA Predictor API!"}

@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}

@app.post("/predict")
def predict_prop(req: PropRequest):
    try:
        player_list = players.find_players_by_full_name(req.player_name)
        if not player_list:
            return {"error": "Player not found. Please check the player name and try again."}
        
        player = player_list[0]
        gamelog = playergamelog.PlayerGameLog(player_id=player['id'], season='2024-25')
        df = gamelog.get_data_frames()[0]
        
        # Debug: Print the DataFrame columns
        print("Available columns in DataFrame:", df.columns)

        # Map the user-friendly stat name to the actual column name
        stat_column = STAT_MAPPING.get(req.stat.lower())
        if not stat_column:
            return {"error": f"Stat '{req.stat}' is not valid. Available stats: {list(STAT_MAPPING.keys())}"}

        if stat_column not in df.columns:
            return {"error": f"Stat '{req.stat}' not found in the data. Available stats: {list(df.columns)}"}
        
        df = df.sort_values("GAME_DATE").tail(10)
        avg = df[stat_column].mean()
        return {"prediction": round(avg, 1)}
    except ReadTimeout:
        return {"error": "The request to stats.nba.com timed out. Please try again later."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
