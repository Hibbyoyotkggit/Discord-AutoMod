import discord
from discord.ext import commands
from discord.utils import get

import random
import logging

from modules import functions

class Greeting(commands.Cog):
    def __init__(self, bot, configs, moduleStates, guildLogger):
        self.bot = bot
        self.configs = configs
        self.moduleStates = moduleStates
        self.guildLogger = guildLogger

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"loaded cog '{self.__class__.__name__.lower()}'")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.moduleStates.isLoaded('logGuildJoinLeave', member.guild.id):
            self.guildLogger[str(member.guild.id)].logGuildJoin(member.name, member.id, member.guild.name, member.guild.id)

        if self.moduleStates.isLoaded('welcome', member.guild.id):
            if (messageConf := self.configs.greeting[str(member.guild.id)]["message"])["use"]:
                channel = member.guild.get_channel(int(messageConf["join"]["channel"]))
                text = ""
                if len(messageConf["join"]["texts"]) > 1 and messageConf["join"]["randomText"]:
                    text = messageConf["join"]["texts"][random.randint(0, len(messageConf["join"]["texts"]))]
                elif len(messageConf["join"]["texts"]) > 0:
                    text = messageConf["join"]["texts"][0]
                text = text.format(memberName=member.name,memberId=member.id)
                await channel.send(text)

            if (embedConf := self.configs.greeting[str(member.guild.id)]["embed"])["use"]:
                embed = discord.Embed()

                title = ""
                if len(embedConf["join"]["titles"]) > 1 and embedConf["join"]["chooseRandomTitle"]:
                    title = embedConf["join"]["titles"][random.randint(0, len(embedConf["join"]["titles"])-1)]
                elif len(embedConf["join"]["titles"]) > 0:
                    title = embedConf["join"]["titles"][0]
                embed.title = title.format(memberName=member.name, memberId=member.id)

                description = ""
                if len(embedConf["join"]["descriptions"]) > 1 and embedConf["join"]["chooseRandomDescription"]:
                    description = embedConf["join"]["descriptions"][random.randint(0, len(embedConf["join"]["descriptions"])-1)]
                elif len(embedConf["join"]["descriptions"]) > 0:
                    description = embedConf["join"]["descriptions"][0]
                embed.description = description.format(memberName=member.name, memberId=member.id)

                embed.color = embedConf["join"]["color"]

                if embedConf["join"]["useAvatar"]:
                    embed.set_thumbnail(url=member.avatar_url)

                channel = member.guild.get_channel(int(embedConf["join"]["channel"]))
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.moduleStates.isLoaded('logGuildJoinLeave', member.guild.id):
            self.guildLogger[str(member.guild.id)].logGuildLeave(member.name, member.id, member.guild.name, member.guild.id)

        if self.moduleStates.isLoaded('disband', member.guild.id):
            if (messageConf := self.configs.greeting[str(member.guild.id)]["message"])["use"]:
                channel = member.guild.get_channel(int(messageConf["leave"]["channel"]))
                text = ""
                if len(messageConf["leave"]["texts"]) > 1 and messageConf["leave"]["randomText"]:
                    text = messageConf["leave"]["texts"][random.randint(0, len(messageConf["leave"]["texts"]))]
                elif len(messageConf["leave"]["texts"]) > 0:
                    text = messageConf["leave"]["texts"][0]
                text = text.format(memberName=member.name, memberId=member.id)
                await channel.send(text)

            if (embedConf := self.configs.greeting[str(member.guild.id)]["embed"])["use"]:
                embed = discord.Embed()

                title = ""
                if len(embedConf["leave"]["titles"]) > 1 and embedConf["leave"]["chooseRandomTitle"]:
                    title = embedConf["leave"]["titles"][random.randint(0, len(embedConf["leave"]["titles"])-1)]
                elif len(embedConf["leave"]["titles"]) > 0:
                    title = embedConf["leave"]["titles"][0]
                embed.title = title.format(memberName=member.name, memberId=member.id)

                description = ""
                if len(embedConf["leave"]["descriptions"]) > 1 and embedConf["leave"]["chooseRandomDescription"]:
                    description = embedConf["leave"]["descriptions"][random.randint(0, len(embedConf["leave"]["descriptions"])-1)]
                elif len(embedConf["leave"]["descriptions"]) > 0:
                    description = embedConf["leave"]["descriptions"][0]
                embed.description = description.format(memberName=member.name, memberId=member.id)

                embed.color = embedConf["leave"]["color"]

                if embedConf["leave"]["useAvatar"]:
                    embed.set_thumbnail(url=member.avatar_url)

                channel = member.guild.get_channel(int(embedConf["leave"]["channel"]))
                await channel.send(embed=embed)
