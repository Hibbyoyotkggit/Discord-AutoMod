import re

def get_channel(guildId, channelId, bot):
    guild = bot.get_guild(int(guildId))
    channel = guild.get_channel(int(channelId))

    return channel

def activeVoiceChannels(channels):
    count = 0
    for channel in channels:
        if len(channel.members) > 0:
            count += 1

    return count

def onBlacklist(blacklist, message):
    messageLower = message.lower().replace(' ','')

    for word in blacklist:
        if word in messageLower:
            return True

    return False

def containsLink(message):
    reString = r".*https?:.*\.[a-zA-Z]{2,3}.*"

    if re.fullmatch(reString, message, re.I):
        return True

    return False
