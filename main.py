import discord
import json

from discord.ext import commands
from discord.utils import get

with open("configs/mainConfig.json", "r") as config_file:
    mainConfig = json.load(config_file)

with open("configs/token.json", "r") as token_file:
    token = json.load(token_file)["token"]

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=mainConfig["command_prefix"], case_insensitive=mainConfig["case_insensitive"], help_command=mainConfig["help_command"], intents=intents)

@bot.event
async def on_ready():
    print("Bot gestartet")
    return

@bot.event
async def on_message(message):
    print(message)
    await bot.process_commands(message)

bot.run(token)
