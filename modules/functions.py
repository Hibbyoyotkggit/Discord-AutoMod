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

def replaceWhitespace(text):
    if type(text) != str:
        return ''

    return re.sub(' *', '', text)

def onBlacklist(blacklist, message):
    messageLower = replaceWhitespace(message) # replace whitespace

    for word in blacklist:
        if re.match(f'.*{word}.*', messageLower, re.I):
            return True

    return False

def containsLink(message):
    messageLower = replaceWhitespace(message)
    reString = r".*https?:.*\.[a-zA-Z]{2,3}.*"

    if re.fullmatch(reString, messageLower, re.I):
        return True

    return False
