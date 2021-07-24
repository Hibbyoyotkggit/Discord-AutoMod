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

configs = configLoader.Configs("configs",["mainConfig.json","token.json","logger.json","group_textchannel.json","autoGenChannel.json"])

intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True

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

if moduleStates.isLoaded('logJoinLeaveChannel'):
	voiceChannelLogger = logger.VoiceChannelLogger(f"{configs.logger['directory']}/{configs.logger['voiceChannelLoggerBaseFilename']}")
	voiceChannelLogger.initFile()

@bot.event
async def on_ready():
	logging.info("Bot is running...")

	if moduleStates.isLoaded('autoGenChannel'):
		guild = bot.get_guild(configs.mainConfig["guild"])
		category = guild.get_channel(configs.autoGenChannel["category"])

		logging.info(category.voice_channels)

		if len(category.voice_channels) == 0:
			await category.create_voice_channel("Channel1")

		return

@bot.event
async def on_message(message):
	if moduleStates.isLoaded('messageLogger'):
		messageLogger.logMessage(message.author, message.author.id, message.content, message.id)
	await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
	if moduleStates.isLoaded('logJoinLeaveChannel'):
		if before.channel == None and after.channel != None:
			voiceChannelLogger.logJoin(member.name, member.id, after.channel.name, after.channel.id)
		elif before.channel != None and after.channel == None:
			voiceChannelLogger.logLeave(member.name, member.id, before.channel.name, before.channel.id)
		elif before.channel != None and after.channel != None and before.channel != after.channel:
			voiceChannelLogger.logMove(member.name, member.id, before.channel.name, before.channel.id, after.channel.name, after.channel.id)

@bot.command(alias=[])
async def clearChannel(ctx):
	if not moduleStates.isLoaded('clearChannel'):
		return

	await ctx.channel.purge()
	textchannelLogger.logClearChannel(ctx.author, ctx.author.id, ctx.channel.name, ctx.channel.id)

bot.run(token)
