import json

class Configs():
    def __init__(self, directory, filenames):
        self.directory = directory

        for filename in filenames:
            try:
                self.__getattribute__(filename.split(".")[0])
            except AttributeError:
                self.__setattr__(filename.split(".")[0], self.readFile(filename))

    def readFile(self,filename):
        with open(f"{self.directory}/{filename}") as file:
            text = json.load(file)

        return text
