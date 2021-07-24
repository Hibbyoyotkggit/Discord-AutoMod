import os
import json

class ModuleStates():
    def __init__(self, directory, mainConfigFile):
        self.directory = directory
        self.mainConfigFile = mainConfigFile

        self.loadedGroups = []
        self.loadedModules = []

        self.readStates()

    def readStates(self):
        if not self.fileExists(self.mainConfigFile):
            return

        mainConfig = self.readFile(self.mainConfigFile)
        if mainConfig.get("active_modules") != None:
            for module in mainConfig["active_modules"]:
                self.loadedModules.append(module)

        if mainConfig.get("active_groups") != None:
            for group in mainConfig["active_groups"]:
                self.readStatesOfGroup(group)

    def readStatesOfGroup(self, group):
        self.loadedGroups.append(group)

        groupFile = f"group_{group}.json"
        if not self.fileExists(groupFile):
            return

        groupConfig = self.readFile(groupFile)
        if groupConfig.get("active_modules") != None:
            for module in groupConfig["active_modules"]:
                self.loadedModules.append(module)

        if groupConfig.get("active_groups") != None:
            for group in groupConfig["active_groups"]:
                self.readStatesOfGroup(group)

    def fileExists(self, filename):
        return os.path.exists(f"{self.directory}/{filename}")

    def readFile(self, filename):
        with open(f"{self.directory}/{filename}") as file:
            text = json.load(file)

        return text

    def isLoaded(self,name):
        return True if name in self.loadedGroups or name in self.loadedModules else False
