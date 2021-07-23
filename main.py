# importing discord.py stuff
import discord
from discord.ext import commands
from discord.utils import get

# importing system libraries
import logging
import sys, os
import json

# importing bot modules
from modules import logger

logging.basicConfig(level=logging.INFO,
	stream=sys.stdout,
	style="{",
	format="{asctime} ({module} : {funcName} : {lineno}) [{levelname:8}] {message}",
	datefmt="%d.%m.%Y %H:%M:%S")

with open("configs/mainConfig.json", "r") as config_file:
    mainConfig = json.load(config_file)

with open("configs/token.json", "r") as token_file:
    token = json.load(token_file)["token"]

with open("configs/messageLogger.json") as json_file:
	messageLoggerConfig = json.load(json_file)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=mainConfig["command_prefix"], case_insensitive=mainConfig["case_insensitive"], help_command=mainConfig["help_command"], intents=intents)

# initialise modules
useMessageLogger = True if "messageLogger" in mainConfig["active_modules"] else False

if useMessageLogger:
	try:
		os.mkdir(messageLoggerConfig["directory"])
	except FileExistsError:
		pass

	messageLogger = logger.MessageLogger(f"{messageLoggerConfig['directory']}/{messageLoggerConfig['baseFilename']}")

@bot.event
async def on_ready():
    logging.info("Bot is running...")
    return

@bot.event
async def on_message(message):
	if useMessageLogger:
		messageLogger.logMessage(message.author, message.author.id, message.content, message.id)
	await bot.process_commands(message)

bot.run(token)
