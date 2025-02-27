import requests
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")

def get_match_history(gameName: str, tagLine: str, count: int = 5):
    """ Fetch the last 'count' matches of a player """
    try:
        # Get PUUID from Riot ID
        puuid_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={API_KEY}"
        puuid = requests.get(puuid_url).json()["puuid"]
        
        # Get Match History (Match IDs)
        match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={API_KEY}"
        match_ids = requests.get(match_url).json()

        return match_ids
    except Exception as e:
        return {"error": str(e)}

def get_match_details(match_id: str):
    """ Fetch full details of a match using its Match ID """
    try:
        match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
        match_data = requests.get(match_url).json()
        
        return match_data
    except Exception as e:
        return {"error": str(e)}
