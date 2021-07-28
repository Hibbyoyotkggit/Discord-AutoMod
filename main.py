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
logging.info(moduleStates.loadedGuilds)

messageLogger = {}
textChannelLogger = {}
voiceChannelLogger = {}

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

@bot.event
async def on_ready():
	logging.info("Bot is running...")

	for guildId in moduleStates.loadedGuilds.keys():
		if moduleStates.isLoaded('autoGenChannel', guildId):
			category = functions.get_channel(int(guildId), configs.autoGenChannel[guildId]["category"], bot)

			logging.info(category.voice_channels)

			if len(category.voice_channels) == 0:
				await category.create_voice_channel("Channel")

@bot.event
async def on_message(message):
	guildId = str(message.guild.id)
	if moduleStates.isLoaded('messageLogger', guildId):
		messageLogger[guildId].logMessage(message.author, message.author.id, message.content, message.id)

	if moduleStates.isLoaded('wordBlacklist', guildId):
		if functions.onBlacklist(configs.blacklist[guildId]["blacklist"],message.content):
			if moduleStates.isLoaded('messageLogger', guildId):
				textChannelLogger[guildId].logMessageDeleteBlacklist(message.content, message.id, message.author.name, message.author.id)
			await message.delete()

	if moduleStates.isLoaded('linkBlocker', guildId):
		if functions.containsLink(message.content):
			if moduleStates.isLoaded('messageLogger', guildId):
				textChannelLogger[guildId].logMessageDeleteLink(message.content, message.id, message.author.name, message.author.id)
			await message.delete()

	await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
	guildId = str(message.guild.id)
	if moduleStates.isLoaded('messageLogger', guildId):
		messageLogger[guildId].logDelete(message.content, message.id, message.author.name, message.author.id)

@bot.event
async def on_voice_state_update(member, before, after):
	guildIds = []
	if before.channel != None: guildIds.append(before.channel.guild.id)
	if after.channel != None: guildIds.append(after.channel.guild.id)

	action = 0 # 0 = default; 1 = join; 2 = move; 3 = leave
	if before.channel == None and after.channel != None: action = 1
	if before.channel != None and after.channel != None: action = 2
	if before.channel != None and after.channel == None: action = 3

	if action == 0:
		return

	for guildId in guildIds:
		if moduleStates.isLoaded('autoGenChannel', str(guildId)):
			category = functions.get_channel(guildId, configs.autoGenChannel[str(guildId)]["category"], bot)
			doCheck = True if before.channel in category.voice_channels or after.channel in category.voice_channels else False

		if action == 1:
			if moduleStates.isLoaded('logJoinLeaveChannel', str(guildId)):
				voiceChannelLogger[str(guildId)].logJoin(member.name, member.id, after.channel.name, after.channel.id)

			if moduleStates.isLoaded('autoGenChannel', str(guildId)) and doCheck:
				if functions.activeVoiceChannels(category.voice_channels) == len(category.voice_channels):
					await category.create_voice_channel("Channel")

		elif action == 2:
			if moduleStates.isLoaded('logJoinLeaveChannel', str(guildId)):
				voiceChannelLogger[str(guildId)].logMove(member.name, member.id, before.channel.name, before.channel.id, after.channel.name, after.channel.id)

			if moduleStates.isLoaded('autoGenChannel', str(guildId)) and doCheck:
				if functions.activeVoiceChannels(category.voice_channels) == len(category.voice_channels):
					await category.create_voice_channel("Channel")

				for channel in category.voice_channels:
					if functions.activeVoiceChannels(category.voice_channels) < len(category.voice_channels)-1:
						if len(channel.members) == 0:
							await channel.delete()
					else:
						break

		elif action == 3:
			if moduleStates.isLoaded('logJoinLeaveChannel', str(guildId)):
				voiceChannelLogger[str(guildId)].logLeave(member.name, member.id, before.channel.name, before.channel.id)

			if moduleStates.isLoaded('autoGenChannel', str(guildId)) and doCheck:
				for channel in category.voice_channels:
					if functions.activeVoiceChannels(category.voice_channels) < len(category.voice_channels)-1:
						if len(channel.members) == 0:
							await channel.delete()
					else:
						break

@bot.command(alias=[])
async def clearChannel(ctx):
	guildId = str(ctx.message.guild.id)
	if not moduleStates.isLoaded('clearChannel', guildId):
		return

	await ctx.channel.purge()
	textChannelLogger[guildId].logClearChannel(ctx.author, ctx.author.id, ctx.channel.name, ctx.channel.id)

bot.run(token)
