import json

class Configs():
    def __init__(self, directory, filenames):
        self.directory = directory

        for filename, attributename in filenames:
            if attributename not in self.__dict__.keys():
                self.__setattr__(attributename, self.readFile(filename))

    def readFile(self,filename):
        with open(f"{self.directory}/{filename}") as file:
            text = json.load(file)

        return text
