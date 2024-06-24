import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('RIOT_API_KEY')

def get_puuid(game_name, tag_line):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['puuid']

def get_account_by_puuid(puuid):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(data)
    return data['id']

def get_current_game_info(summoner_id):
    url = f"https://americas.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_champion_mastery(puuid, champion_id):
    url = f"https://americas.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}?api_key={api_key}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
