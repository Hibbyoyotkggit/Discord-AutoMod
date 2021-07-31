import datetime

class Logger():
    def __init__(self, baseFilename):
        self.baseFilename = baseFilename
        self.filename = f"{baseFilename}-{datetime.datetime.now().strftime('%d_%b_%H:%M:%S')}.log"

    def initFile(self):
        with open(self.filename, "a") as file:
            file.write("")

class MessageLogger(Logger):
    def logMessage(self,author, authorId, message, messageId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} by '{author}' ({authorId}): '{message}' ({messageId})\n")

    def logDelete(self, message, messageId, author, authorId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{message}' ({messageId}) by '{author}' ({authorId}) was deleted\n")

class TextChannelLogger(Logger):
    def logClearChannel(self, author, authorId, channel, channelId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} cleared Channel '{channel}' ({channelId}) invoked by '{author}' ({authorId})\n")

    def logMessageDeleteBlacklist(self, message, messageId, author, authorId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{message}' ({messageId}) by '{author}' ({authorId}) was deleted (blacklist)\n")

    def logMessageDeleteLink(self, message, messageId, author, authorId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{message}' ({messageId}) by '{author}' ({authorId}) was deleted (link)\n")


class VoiceChannelLogger(Logger):
    def logJoin(self, member, memberId, channel, channelId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{member}' ({memberId}) joind voice channel '{channel}' ({channelId})\n")

    def logLeave(self, member, memberId, channel, channelId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{member}' ({memberId}) left voice channel '{channel}' ({channelId})\n")

    def logMove(self, member, memberId, beforeChannel, beforeChannelId, afterChannel, afterChannelId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{member}' ({memberId}) moved from voice channel '{beforeChannel}' ({beforeChannelId}) to '{afterChannel}' ({afterChannelId})\n")

class GuildJoinLeaveLogger(Logger):
    def logGuildJoin(self, member, memberId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{member}' ({memberId}) joind the guild\n")

    def logGuildLeave(self, member, memberId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} '{member}' ({memberId}) left the guild\n")
