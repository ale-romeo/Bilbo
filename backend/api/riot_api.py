import requests
import os
import time
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")

# Global Request Counter
request_count = 0
start_time = time.time()

def rate_limiter():
    """Enforce Riot API rate limits"""
    global request_count, start_time
    
    # If we hit 20 requests in 1 second, wait before next request
    if request_count >= 20:
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)
        request_count = 0
        start_time = time.time()

    # If we hit 100 requests in 2 minutes, wait before next request
    if request_count >= 100:
        elapsed_time = time.time() - start_time
        if elapsed_time < 120:
            time.sleep(120 - elapsed_time)
        request_count = 0
        start_time = time.time()
    
    request_count += 1

def fetch_data(url):
    """Wrapper function to handle rate limits & API requests"""
    rate_limiter()
    response = requests.get(url)
    
    # Retry if rate limited
    if response.status_code == 429:
        print("⚠️ Rate limit exceeded! Waiting 10 seconds...")
        time.sleep(10)
        return fetch_data(url)
    
    return response.json()

def get_challenger_summoners(region="EUW1"):
    """Fetch all summoners in Challenger rank"""
    url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}"
    entries = fetch_data(url)["entries"]
    summoners = [entry["puuid"] for entry in entries]
    return summoners

def get_match_ids(puuid, region="europe"):
    """Fetch match IDs for a given summoner"""
    match_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}"
    match_ids = fetch_data(match_url)
    
    return match_ids
