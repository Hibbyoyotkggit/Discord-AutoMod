import os
import json

class ModuleStates():
    def __init__(self, directory, mainConfigFile):
        self.directory = directory
        self.mainConfigFile = mainConfigFile

        self.loadedGuilds = {}

        self.readStates()

    def readStates(self):
        if not self.fileExists(self.mainConfigFile):
            return

        mainConfig = self.readFile(self.mainConfigFile)
        if mainConfig.get("guilds") != None:
            for guildId in mainConfig["guilds"].keys():
                guild = mainConfig["guilds"][guildId]

                self.loadedGuilds[guildId] = {"active_modules": [], "active_groups": []}

                if guild.get("active_modules") != None:
                    for module in guild["active_modules"]:
                        self.loadedGuilds[guildId]["active_modules"].append(module)

                if guild.get("active_groups") != None:
                    for group in guild["active_groups"]:
                        self.loadedGuilds[guildId]["active_groups"].append(group)

                        self.readStatesOfGroup(group, guildId)

    def readStatesOfGroup(self, group, guildId):
        groupFile = f"group_{group}.json"
        if not self.fileExists(groupFile):
            return


        groupConfig = self.readFile(groupFile)
        if groupConfig.get(str(guildId)) != None:
            guild = groupConfig[str(guildId)]

            if guild.get("active_modules") != None:
                for module in guild["active_modules"]:
                    self.loadedGuilds[str(guildId)]["active_modules"].append(module)

            if guild.get("active_groups") != None:
                for group in guild["active_groups"]:
                    self.readStatesOfGroup(group, str(guildId))

    def fileExists(self, filename):
        return os.path.exists(f"{self.directory}/{filename}")

    def readFile(self, filename):
        with open(f"{self.directory}/{filename}") as file:
            text = json.load(file)

        return text

    def isLoaded(self, name, guildId):
        guildId = str(guildId)
        if guildId not in self.loadedGuilds.keys():
            return False
        return True if name in (guild := self.loadedGuilds[guildId])["active_modules"] or name in guild["active_groups"] else False
