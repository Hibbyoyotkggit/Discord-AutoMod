import shutil
import os, sys
import json

start = input("All existing config files will be overridden! To you wan't to go on? [y/N]: ")
if start.lower() != "y":
    sys.exit()

for file in os.listdir('configs/defaults'):
    if os.path.isfile(f'configs/defaults/{file}') == False:
        continue

    shutil.copyfile(f'configs/defaults/{file}', f'configs/{file}')

mainGuildId = input("Insert guild id: ")


with open('configs/mainConfig.json', 'r') as file:
    mainConfig = json.load(file)

with open('configs/autoGenChannel.json', 'r') as file:
    autoGenChannelConfig = json.load(file)

with open('configs/blacklist.json', 'r') as file:
    blacklist = json.load(file)

with open('configs/group_textchannel.json', 'r') as file:
    textchannelConfig = json.load(file)

with open('configs/group_voicechannel.json', 'r') as file:
    voicechannelConfig = json.load(file)

with open('configs/logger.json', 'r') as file:
    loggerConfig = json.load(file)

with open('configs/token.json', 'r') as file:
    token = json.load(file)

# main config
prefix = input(f"Command prefix? [{mainConfig['command_prefix']}]: ")
if prefix == "":
    prefix = mainConfig['command_prefix']

mainConfig['command_prefix'] = prefix

case = input("Case insensitive? [Y/n]: ")
if case == "n":
    mainConfig['case_insensitive'] = False

defaultGuildConf = mainConfig["guilds"]["GUILDID"]
del mainConfig["guilds"]["GUILDID"]

mainConfig["guilds"][mainGuildId] = defaultGuildConf

for group in mainConfig["guilds"][mainGuildId]["active_groups"][:]:
    activate = input(f'Do you want to activate group \'{group}\' for guild \'{mainGuildId}\'? [Y/n]: ')
    if activate.lower() == "n":
        mainConfig["guilds"][mainGuildId]["active_groups"].remove(group)

# textchannel
if 'textchannel' in mainConfig["guilds"][mainGuildId]["active_groups"]:
    defaultTextChannelConfig = textchannelConfig["GUILDID"]
    del textchannelConfig["GUILDID"]
    textchannelConfig[mainGuildId] = defaultTextChannelConfig

    for module in textchannelConfig[mainGuildId]["active_modules"][:]:
        activate = input(f'Do you want to activate module \'{module}\' for guild \'{mainGuildId}\'? [Y/n]: ')
        if activate.lower() == "n":
            textchannelConfig[mainGuildId]["active_modules"].remove(module)

    if 'wordBlacklist' in textchannelConfig[mainGuildId]["active_modules"]:
        defaultBlacklist = blacklist["GUILDID"]
        del blacklist["GUILDID"]
        blacklist[mainGuildId] = defaultBlacklist

if 'voicechannel' in mainConfig["guilds"][mainGuildId]["active_groups"]:
    defaultVoiceChannelConfig = voicechannelConfig["GUILDID"]
    del voicechannelConfig["GUILDID"]
    voicechannelConfig[mainGuildId] = defaultVoiceChannelConfig

    for module in voicechannelConfig[mainGuildId]["active_modules"][:]:
        activate = input(f'Do you want to activate module \'{module}\' for guild \'{mainGuildId}\'? [Y/n]: ')
        if activate.lower() == "n":
            voicechannelConfig[mainGuildId]["active_modules"].remove(module)

    if 'autoGenChannel' in voicechannelConfig[mainGuildId]["active_modules"]:
        del autoGenChannelConfig["GUILDID"]
        autoGenChannelConfig[mainGuildId] = {}

        categoryId = input("Insert category id for autoGenChannel module: ")
        autoGenChannelConfig[mainGuildId]["category"] = categoryId

# logger
defaultLoggerConfig = loggerConfig["GUILDID"]
del loggerConfig["GUILDID"]
loggerConfig[mainGuildId] = defaultLoggerConfig

# token
tokenInp = input("Insert token: ")
token["token"] = tokenInp

with open('configs/mainConfig.json', 'w') as file:
    json.dump(mainConfig, file, indent=2)

with open('configs/autoGenChannel.json', 'w') as file:
    json.dump(autoGenChannelConfig, file, indent=2)

with open('configs/blacklist.json', 'w') as file:
    json.dump(blacklist, file, indent=2)

with open('configs/group_textchannel.json', 'w') as file:
    json.dump(textchannelConfig, file, indent=2)

with open('configs/group_voicechannel.json', 'w') as file:
    json.dump(voicechannelConfig, file, indent=2)

with open('configs/logger.json', 'w') as file:
    json.dump(loggerConfig, file, indent=2)

with open('configs/token.json', 'w') as file:
    json.dump(token, file, indent=2)
