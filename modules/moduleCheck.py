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
        for module in mainConfig["active_modules"]:
            self.loadedModules.append(module)

        for group in mainConfig["active_groups"]:
            self.loadedGroups.append(group)

            groupFile = f"group_{group}.json"
            if not self.fileExists(groupFile):
                continue

            groupConfig = self.readFile(groupFile)
            for module in groupConfig["active_modules"]:
                self.loadedModules.append(module)

    def fileExists(self, filename):
        return os.path.exists(f"{self.directory}/{filename}")

    def readFile(self, filename):
        with open(f"{self.directory}/{filename}") as file:
            text = json.load(file)

        return text

    def isLoaded(self,name):
        return True if name in self.loadedGroups or name in self.loadedModules else False
