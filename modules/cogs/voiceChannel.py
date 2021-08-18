import discord
from discord.ext import commands
from discord.utils import get

import logging

from modules import functions

class VoiceChannel(commands.Cog):
    def __init__(self, bot, configs, moduleStates, voiceChannelLogger):
        self.bot = bot
        self.configs = configs
        self.moduleStates = moduleStates
        self.voiceChannelLogger = voiceChannelLogger

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"loaded cog '{self.__class__.__name__.lower()}'")

        await self.initialAutoGenCheck()

    async def initialAutoGenCheck(self):
        for guildId in self.moduleStates.loadedGuilds.keys():
            if self.moduleStates.isLoaded('autoGenChannel', guildId):
                category = functions.get_channel(int(guildId), self.configs.autoGenChannel[guildId]["category"], self.bot)

                if len(category.voice_channels) == 0:
                    await category.create_voice_channel("Channel")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guildId = before.channel.guild.id if before.channel != None else (after.channel.guild.id if after.channel != None else None)
        if guildId == None:
            return

        action = await self.findAction(before, after)

        if action == 0:
            return

        category, doCheck = await self.findAutoGenChannelInfos(guildId, before, after)

        if action == 1:
            await self.on_join(guildId, member, after, category, doCheck)

        elif action == 2:
            await self.on_move(guildId, member, before, after, category, doCheck)

        elif action == 3:
            await self.on_leave(guildId, member, before, category, doCheck)

    async def findAction(self, before, after):
        action = 0 # 0 = default; 1 = join; 2 = move; 3 = leave
        if before.channel == None and after.channel != None: action = 1
        if before.channel != None and after.channel != None: action = 2
        if before.channel != None and after.channel == None: action = 3

        return action

    async def findAutoGenChannelInfos(self, guildId, before, after):
        if self.moduleStates.isLoaded('autoGenChannel', guildId):
            category = functions.get_channel(guildId, self.configs.autoGenChannel[str(guildId)]["category"], self.bot)
            doCheck = True if before.channel in category.voice_channels or after.channel in category.voice_channels else False
        else:
            category = None
            doCheck = None

        return (category, doCheck)

    async def on_join(self, guildId, member, after, category, doCheck):
        if self.moduleStates.isLoaded('logJoinLeaveChannel', guildId):
            self.voiceChannelLogger[str(guildId)].logJoin(member.name, member.id, after.channel.name, after.channel.id)

        await self.on_join_(guildId, category, doCheck)

    async def on_join_(self, guildId, category, doCheck):
        if self.moduleStates.isLoaded('autoGenChannel', guildId) and doCheck:
            if functions.activeVoiceChannels(category.voice_channels) == len(category.voice_channels):
                await category.create_voice_channel("Channel")

    async def on_leave(self, guildId, member, before, category, doCheck):
        if self.moduleStates.isLoaded('logJoinLeaveChannel', guildId):
            self.voiceChannelLogger[str(guildId)].logLeave(member.name, member.id, before.channel.name, before.channel.id)

        await self.on_leave_(guildId, category, doCheck)


    async def on_leave_(self, guildId, category, doCheck):
        if self.moduleStates.isLoaded('autoGenChannel', guildId) and doCheck:
            for channel in category.voice_channels:
                if functions.activeVoiceChannels(category.voice_channels) < len(category.voice_channels)-1:
                    if len(channel.members) == 0:
                        await channel.delete()
                else:
                    break

    async def on_move(self, guildId, member, before, after, category, doCheck):
        if self.moduleStates.isLoaded('logJoinLeaveChannel', guildId):
            self.voiceChannelLogger[str(guildId)].logMove(member.name, member.id, before.channel.name, before.channel.id, after.channel.name, after.channel.id)

        await self.on_join_(guildId, category, doCheck)
        await self.on_leave_(guildId, category, doCheck)
