import discord
from discord.ext import commands
from discord.utils import get

import logging

from modules import functions

class TextChannel(commands.Cog):
    def __init__(self, bot, configs, moduleStates, messageLogger, textChannelLogger):
        self.bot = bot
        self.configs = configs
        self.moduleStates = moduleStates
        self.messageLogger = messageLogger
        self.textChannelLogger = textChannelLogger

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"loaded cog '{self.__class__.__name__.lower()}'")

    @commands.Cog.listener()
    async def on_message(self, message):
        guildId = str(message.guild.id)
        if self.moduleStates.isLoaded('messageLogger', guildId):
            self.messageLogger[guildId].logMessage(message.author, message.author.id, message.content, message.id)

        if self.moduleStates.isLoaded('wordBlacklist', guildId):
            await self.execute_blacklist(message, guildId)

        if self.moduleStates.isLoaded('linkBlocker', guildId):
            await self.execute_linkBlocker(message, guildId)

    async def execute_blacklist(self, message, guildId):
        if functions.onBlacklist(self.configs.blacklist[guildId]["blacklist"],message.content):
            self.textChannelLogger[guildId].logMessageDeleteBlacklist(message.content, message.id, message.author.name, message.author.id)
            await message.delete()

    async def execute_linkBlocker(self, message, guildId):
        if functions.containsLink(message.content):
            self.textChannelLogger[guildId].logMessageDeleteLink(message.content, message.id, message.author.name, message.author.id)
            await message.delete()

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        guildId = str(message.guild.id)
        if self.moduleStates.isLoaded('messageLogger', guildId):
            self.messageLogger[guildId].logDelete(message.content, message.id, message.author.name, message.author.id)

    @commands.command()
    async def clearChannel(self, ctx):
    	guildId = str(ctx.message.guild.id)
    	if not self.moduleStates.isLoaded('clearChannel', guildId):
    		return

    	await ctx.channel.purge()
    	self.textChannelLogger[guildId].logClearChannel(ctx.author, ctx.author.id, ctx.channel.name, ctx.channel.id)
