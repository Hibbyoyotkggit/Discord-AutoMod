# importing discord.py stuff
import discord
from discord.ext import commands
from discord.utils import get

# importing system libraries
import logging
import sys, os
import json

# importing bot modules
from modules import configLoader, moduleCheck, logger, functions, cogs

logging.basicConfig(level=logging.INFO,
	stream=sys.stdout,
	style="{",
	format="{asctime} ({module} : {funcName} : {lineno}) [{levelname:8}] {message}",
	datefmt="%d.%m.%Y %H:%M:%S")

configFiles = ["mainConfig.json","token.json","logger.json","group_textchannel.json","autoGenChannel.json","blacklist.json","group_greeting.json"]
configs = configLoader.Configs("configs",configFiles)

intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix=configs.mainConfig["command_prefix"], case_insensitive=configs.mainConfig["case_insensitive"], help_command=configs.mainConfig["help_command"], intents=intents)
token = configs.token["token"]

# initialise modules

moduleStates = moduleCheck.ModuleStates("configs","mainConfig.json")
logging.info(moduleStates.loadedGuilds)

messageLogger = {}
textChannelLogger = {}
voiceChannelLogger = {}
guildLogger = {}

for guildId in moduleStates.loadedGuilds.keys():
	if moduleStates.isLoaded('messageLogger', guildId) or moduleStates.isLoaded('textchannel', guildId) or moduleStates.isLoaded('logJoinLeaveChannel', guildId):
		try:
			os.mkdir(configs.logger[guildId]['directory'])
		except FileExistsError:
			pass

	if moduleStates.isLoaded('messageLogger', guildId):
		messageLogger[guildId] = logger.MessageLogger(f"{configs.logger[guildId]['directory']}/{configs.logger[guildId]['messageLoggerBaseFilename']}")
		messageLogger[guildId].initFile()

	if moduleStates.isLoaded('textchannel', guildId):
		textChannelLogger[guildId] = logger.TextChannelLogger(f"{configs.logger[guildId]['directory']}/{configs.logger[guildId]['textChannelLoggerBaseFilename']}")
		textChannelLogger[guildId].initFile()

	if moduleStates.isLoaded('logJoinLeaveChannel', guildId):
		voiceChannelLogger[guildId] = logger.VoiceChannelLogger(f"{configs.logger[guildId]['directory']}/{configs.logger[guildId]['voiceChannelLoggerBaseFilename']}")
		voiceChannelLogger[guildId].initFile()

	if moduleStates.isLoaded('logGuildJoinLeave', guildId):
		guildLogger[guildId] = logger.GuildJoinLeaveLogger(f"{configs.logger[guildId]['directory']}/{configs.logger[guildId]['guildLoggerBaseFilename']}")
		guildLogger[guildId].initFile()

# register cogs
bot.add_cog(cogs.Greeting(bot, configs, moduleStates, guildLogger))
bot.add_cog(cogs.TextChannel(bot, configs, moduleStates, messageLogger, textChannelLogger))
bot.add_cog(cogs.VoiceChannel(bot, configs, moduleStates, voiceChannelLogger))

@bot.event
async def on_ready():
	logging.info("Bot is running...")

@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.command(alias=[])
async def stopBot(ctx):
	await bot.close()

bot.run(token)
