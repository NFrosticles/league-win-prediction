import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from data.riot_api import get_puuid, get_current_game_info, get_champion_mastery, get_account_by_puuid
from models.predict_model import preprocess_and_predict

#test
# Load environment variables from .env file
load_dotenv()

# Get the environment variables
api_key = os.getenv('RIOT_API_KEY')
bot_token = os.getenv('DISCORD_BOT_TOKEN')

# Debugging prints to check if variables are loaded
print(f"RIOT_API_KEY: {api_key}")
print(f"DISCORD_BOT_TOKEN: {bot_token}")

# Ensure api_token is not None
if api_key is None:
    raise ValueError("RIOT_API_KEY environment variable is not set")

# Ensure bot_token is not None
if bot_token is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set")



intents = discord.Intents.all()
#intents.messages = True  # Enable message content intent
#intents.guilds = True    # Enable guilds intent
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.get_channel(91277265450582016).send('Bot is now online!')

# Command: Ping
@bot.command()
async def ping(ctx):
    print("Ping command received!")
    await ctx.send('Pong!')


@bot.command()
async def predict(ctx, summoner_name: str, tag_line: str):
    print(f"Predict command received for {summoner_name} - {tag_line}")
    try:
        puuid = get_puuid(summoner_name, tag_line)
        print(f"PUUID: {puuid}")
        summoner_id = get_account_by_puuid(puuid)
        game_info = get_current_game_info(summoner_id)

        predictions = []

        for participant in game_info['participants']:
            champion_id = participant['championId']
            participant_puuid = get_puuid(participant['summonerName'], tag_line)
            mastery_data = get_champion_mastery(participant_puuid, champion_id)

            win_percentage = preprocess_and_predict(mastery_data)
            predictions.append((participant['summonerName'], champion_id, win_percentage))

        # Generate a funny message based on win percentage
        message = ""
        for summoner_name, champion_id, win_percentage in predictions:
            message += f"{summoner_name} playing champion ID {champion_id} has a win percentage of {win_percentage:.2f}%.\n"

        await ctx.send(message)
    except Exception as e:
        await ctx.send(f'Error fetching data: {e}')


bot.run(bot_token)
