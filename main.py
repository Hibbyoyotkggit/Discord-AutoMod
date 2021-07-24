# importing discord.py stuff
import discord
from discord.ext import commands
from discord.utils import get

# importing system libraries
import logging
import sys, os
import json

# importing bot modules
from modules import configLoader, moduleCheck, logger

logging.basicConfig(level=logging.INFO,
	stream=sys.stdout,
	style="{",
	format="{asctime} ({module} : {funcName} : {lineno}) [{levelname:8}] {message}",
	datefmt="%d.%m.%Y %H:%M:%S")

configs = configLoader.Configs("configs",["mainConfig.json","token.json","logger.json","group_textchannel.json"])

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=configs.mainConfig["command_prefix"], case_insensitive=configs.mainConfig["case_insensitive"], help_command=configs.mainConfig["help_command"], intents=intents)
token = configs.token["token"]

# initialise modules

moduleStates = moduleCheck.ModuleStates("configs","mainConfig.json")
logging.info(moduleStates.loadedModules)

if moduleStates.isLoaded('messageLogger'):
	try:
		os.mkdir(configs.logger["directory"])
	except FileExistsError:
		pass

	messageLogger = logger.MessageLogger(f"{configs.logger['directory']}/{configs.logger['messageLoggerBaseFilename']}")
	messageLogger.initFile()

if moduleStates.isLoaded('textchannel'):
	textchannelLogger = logger.TextChannelLogger(f"{configs.logger['directory']}/{configs.logger['textChannelLoggerBaseFilename']}")
	textchannelLogger.initFile()

@bot.event
async def on_ready():
    logging.info("Bot is running...")
    return

@bot.event
async def on_message(message):
	if moduleStates.isLoaded('messageLogger'):
		messageLogger.logMessage(message.author, message.author.id, message.content, message.id)
	await bot.process_commands(message)

@bot.command(alias=[])
async def clearChannel(ctx):
	if not moduleStates.isLoaded('clearChannel'):
		return

	await ctx.channel.purge()
	textchannelLogger.logClearChannel(ctx.author, ctx.author.id, ctx.channel.name, ctx.channel.id)

bot.run(token)
