import pandas as pd
import time
from riot_api import get_challenger_summoners, get_match_ids, fetch_data, API_KEY

def get_match_details(match_id):
    """Fetch and process match details from Riot API"""
    match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    match_data = fetch_data(match_url)
    
    participants = match_data['info']['participants']
    data = []
    
    for player in participants:
        data.append({
            "match_id": match_id,
            "gameDuration": match_data["info"]["gameDuration"],
            "teamId": player["teamId"],
            "championId": player["championId"],
            "championName": player["championName"],
            "teamPosition": player["teamPosition"],
            "lane": player["lane"],
            "kills": player["kills"],
            "deaths": player["deaths"],
            "assists": player["assists"],
            "goldEarned": player["goldEarned"],
            "damageDealtToChampions": player["totalDamageDealtToChampions"],
            "damageDealtToObjectives": player["damageDealtToObjectives"],
            "damageTaken": player["totalDamageTaken"],
            "visionScore": player["visionScore"],
            "wardsPlaced": player["wardsPlaced"],
            "wardTakedowns": player.get("wardTakedowns", 0),
            "timePlayed": player["timePlayed"],
            "baronKills": player["baronKills"],
            "dragonKills": player["dragonKills"],
            "turretKills": player["turretKills"],
            "firstBloodKill": player["firstBloodKill"],
            "firstBloodAssist": player["firstBloodAssist"],
            "jungleCsBefore10Minutes": player.get("jungleCsBefore10Minutes", 0),
            "enemyJungleMonsterKills": player.get("enemyJungleMonsterKills", 0),
            "items_bought": [player.get(f"item{i}", 0) for i in range(6)],
            "runes": player.get("perks", {}),
            "win": 1 if player["win"] else 0
        })
    
    return data

def collect_challenger_data():
    """Fetch match data for 100 Challenger players with rate limit handling"""
    challenger_summoners = get_challenger_summoners()
    all_match_ids = []

    for summoner in challenger_summoners:
        match_ids = get_match_ids(summoner)
        all_match_ids.extend(match_ids)
        if len(all_match_ids) >= 10000:
            break
        time.sleep(1)  # Prevent API rate limits

    all_match_ids = list(set(all_match_ids))  # Remove duplicates

    all_match_data = []
    for i, match_id in enumerate(all_match_ids):
        all_match_data.extend(get_match_details(match_id))

        # Prevent exceeding Riot API rate limits
        if (i + 1) % 20 == 0:
            print("⏳ Reached 20 requests, waiting 1 second...")
            time.sleep(1)
        if (i + 1) % 100 == 0:
            print("⏳ Reached 100 requests, waiting 2 minutes...")
            time.sleep(120)

    # Save to CSV
    df = pd.DataFrame(all_match_data)
    df.to_csv("challenger_matches.csv", index=False)
    print(f"✅ Saved {len(all_match_ids)} Challenger matches.")

# Run data collection
collect_challenger_data()
