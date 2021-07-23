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

class TextChannelLogger(Logger):
    def logClearChannel(self, author, authorId, channel, channelId):
        with open(self.filename, "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%d %b %H:%M:%S')} cleared Channel '{channel}' ({channelId}) invoked by '{author}' ({authorId})\n")
