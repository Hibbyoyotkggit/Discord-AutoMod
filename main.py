# importing discord.py stuff
import discord
from discord.ext import commands
from discord.utils import get

# importing system libraries
import logging
import sys, os
import json

# importing bot modules
from modules import configLoader, moduleCheck, logger, functions

logging.basicConfig(level=logging.INFO,
	stream=sys.stdout,
	style="{",
	format="{asctime} ({module} : {funcName} : {lineno}) [{levelname:8}] {message}",
	datefmt="%d.%m.%Y %H:%M:%S")

configFiles = ["mainConfig.json","token.json","logger.json","group_textchannel.json","autoGenChannel.json","blacklist.json"]
configs = configLoader.Configs("configs",configFiles)

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
		category = functions.get_channel(configs.mainConfig["guild"], configs.autoGenChannel["category"], bot)

		logging.info(category.voice_channels)

		if len(category.voice_channels) == 0:
			await category.create_voice_channel("Channel")

		return

@bot.event
async def on_message(message):
	if moduleStates.isLoaded('messageLogger'):
		messageLogger.logMessage(message.author, message.author.id, message.content, message.id)

	if moduleStates.isLoaded('wordBlacklist'):
		if functions.onBlacklist(configs.blacklist["blacklist"],message.content):
			if moduleStates.isLoaded('messageLogger'):
				textchannelLogger.logMessageDeleteBlacklist(message.content, message.id, message.author.name, message.author.id)
			await message.delete()

	if moduleStates.isLoaded('linkBlocker'):
		if functions.containsLink(message.content):
			if moduleStates.isLoaded('messageLogger'):
				textchannelLogger.logMessageDeleteLink(message.content, message.id, message.author.name, message.author.id)
			await message.delete()

	await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
	if moduleStates.isLoaded('messageLogger'):
		messageLogger.logDelete(message.content, message.id, message.author.name, message.author.id)

@bot.event
async def on_voice_state_update(member, before, after):
	if moduleStates.isLoaded('autoGenChannel'):
		category = functions.get_channel(configs.mainConfig["guild"], configs.autoGenChannel["category"], bot)
		doCheck = True if before.channel in category.voice_channels or after.channel in category.voice_channels else False

	# join
	if before.channel == None and after.channel != None:
		if moduleStates.isLoaded('logJoinLeaveChannel'):
			voiceChannelLogger.logJoin(member.name, member.id, after.channel.name, after.channel.id)

		if moduleStates.isLoaded('autoGenChannel') and doCheck:
			if functions.activeVoiceChannels(category.voice_channels) == len(category.voice_channels):
				await category.create_voice_channel("Channel")

	# leave
	elif before.channel != None and after.channel == None:
		if moduleStates.isLoaded('logJoinLeaveChannel'):
			voiceChannelLogger.logLeave(member.name, member.id, before.channel.name, before.channel.id)

		if moduleStates.isLoaded('autoGenChannel') and doCheck:
			for channel in category.voice_channels:
				if functions.activeVoiceChannels(category.voice_channels) < len(category.voice_channels)-1:
					if len(channel.members) == 0:
						await channel.delete()
				else:
					break

	# move
	elif before.channel != None and after.channel != None and before.channel != after.channel:
		if moduleStates.isLoaded('logJoinLeaveChannel'):
			voiceChannelLogger.logMove(member.name, member.id, before.channel.name, before.channel.id, after.channel.name, after.channel.id)

		if moduleStates.isLoaded('autoGenChannel') and doCheck:
			if functions.activeVoiceChannels(category.voice_channels) == len(category.voice_channels):
				await category.create_voice_channel("Channel")

			for channel in category.voice_channels:
				if functions.activeVoiceChannels(category.voice_channels) < len(category.voice_channels)-1:
					if len(channel.members) == 0:
						await channel.delete()
				else:
					break

@bot.command(alias=[])
async def clearChannel(ctx):
	if not moduleStates.isLoaded('clearChannel'):
		return

	await ctx.channel.purge()
	textchannelLogger.logClearChannel(ctx.author, ctx.author.id, ctx.channel.name, ctx.channel.id)

bot.run(token)
