# importing discord.py stuff
import discord
from discord.ext import commands
from discord.utils import get

# importing system libraries
import logging
import sys, os
import json

# importing bot modules
from modules import configLoader, logger

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
useMessageLogger = True if "messageLogger" in configs.mainConfig["active_modules"] else False

if useMessageLogger:
	try:
		os.mkdir(configs.logger["directory"])
	except FileExistsError:
		pass

	messageLogger = logger.MessageLogger(f"{configs.logger['directory']}/{configs.logger['messageLoggerBaseFilename']}")
	messageLogger.initFile()

useTextChannelGroup = True if "textchannel" in configs.mainConfig["active_groups"] else False
useClearChannel = True if useTextChannelGroup and "clearChannel" in configs.group_textchannel["active_modules"] else False

if useTextChannelGroup:
	textchannelLogger = logger.TextChannelLogger(f"{configs.logger['directory']}/{configs.logger['textChannelLoggerBaseFilename']}")
	textchannelLogger.initFile()

@bot.event
async def on_ready():
    logging.info("Bot is running...")
    return

@bot.event
async def on_message(message):
	if useMessageLogger:
		messageLogger.logMessage(message.author, message.author.id, message.content, message.id)
	await bot.process_commands(message)

@bot.command(alias=[])
async def clearChannel(ctx):
	if not useClearChannel:
		return

	await ctx.channel.purge()
	textchannelLogger.logClearChannel(ctx.author, ctx.author.id, ctx.channel.name, ctx.channel.id)

bot.run(token)
