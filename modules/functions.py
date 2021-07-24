def get_channel(guildId, channelId, bot):
    guild = bot.get_guild(guildId)
    channel = guild.get_channel(channelId)

    return channel

def activeVoiceChannels(channels):
    count = 0
    for channel in channels:
        if len(channel.members) > 0:
            count += 1

    return count

def onBlacklist(blacklist, message):
    messageLower = message.lower().replace(' ','')
    print(f"'{messageLower}'")

    for word in blacklist:
        if word in messageLower:
            return True

    return False
