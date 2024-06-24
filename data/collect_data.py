import requests

api_key = "" #Subject to change

def get_puuid(game_name, tag_line):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}"
    headers = {
         "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        puuid = data['puuid']
        return puuid
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except KeyError as key_err:
        print(f"KeyError occurred: {key_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Example usage
game_name = ""   # Replace with your Riot Games game name
tag_line = ""     # Replace with your Riot Games tag line
champion_id = 157            # Example champion ID (Yasuo)

# Get summoner's PUUID
puuid = get_puuid(game_name, tag_line)
print(f"Summoner's PUUID: {puuid}")



def get_champion_mastery(puuid, champion_id):
    url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}"
    headers = {
        "X-Riot-Token": api_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Get champion mastery for the specified champion
champion_mastery = get_champion_mastery(puuid, champion_id)
print(f"Champion Mastery for champion ID {champion_id}: {champion_mastery}")


