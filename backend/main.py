from fastapi import FastAPI
from api.riot_api import get_match_history, get_match_details
import uvicorn

app = FastAPI()

app = FastAPI()

@app.get("/matches/{gameName}/{tagLine}")
def fetch_match_history(gameName: str, tagLine: str, count: int = 5):
    return get_match_history(gameName, tagLine, count)

@app.get("/match/{match_id}")
def fetch_match_details(match_id: str):
    return get_match_details(match_id)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
