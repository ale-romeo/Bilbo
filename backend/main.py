from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()  # Load .env file
API_KEY = os.getenv("RIOT_API_KEY")  # Load API Key from .env

@app.get("/")
def read_root():
    return {"message": "Bilbo is running!"}

@app.get("/summoner/{gameName}/{tagLine}")
def get_summoner(gameName: str, tagLine: str):
    puuid_Url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={API_KEY}"
    puuid = (requests.get(puuid_Url)).json()["puuid"]
    summonerUrl = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={API_KEY}"
    summonerData = requests.get(summonerUrl)
    return summonerData.json()

@app.get("/match-history/{gameName}/{tagLine}")
def get_match_history(gameName: str, tagLine: str, count: int = 5):
    """ Fetch the last 'count' matches of a player """
    try:
        # Get PUUID from Riot ID
        puuid_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={API_KEY}"
        puuid = requests.get(puuid_url).json()["puuid"]
        print(puuid)
        
        # Get Match History (Match IDs)
        match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={API_KEY}"
        match_ids = requests.get(match_url).json()
        print(match_ids)

        return match_ids
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
