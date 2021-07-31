import discord
from discord.ext import commands
from discord.utils import get

import logging

class TextChannel(commands.Cog):
    def __init__(self, bot, configs, moduleStates, textChannelLogger):
        self.bot = bot
        self.configs = configs
        self.moduleStates = moduleStates
        self.textChannelLogger = textChannelLogger

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"loaded cog '{self.__class__.__name__.lower()}'")

class MessageLogger(commands.Cog):
    def __init__(self, bot, configs, messageLogger):
        self.bot = bot
        self.configs = configs
        self.messageLogger = messageLogger

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"loaded cog '{self.__class__.__name__.lower()}'")

class VoiceChannel(commands.Cog):
    def __init__(self, bot, configs, moduleStates, voiceChannelLogger):
        self.bot = bot
        self.configs = configs
        self.moduleStates = moduleStates
        self.voiceChannelLogger = voiceChannelLogger

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"loaded cog '{self.__class__.__name__.lower()}'")
