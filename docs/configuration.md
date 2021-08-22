## Configuration

To configure to bot you'll have to edit some json-files. You can find templates for these in _configs/defaults_. Which ones you'll have to edit depends on what you want the bot to do. But the _mainConfig.json_ has to be edited in every case. So let's start off with that one...



### Main

First, copy the template _configs/defaults/mainConfig.json_ into _configs_.

Open it in any text editor you like. It should look like this:

```json
{
  "command_prefix": "?",
  "case_insensitive": true,
  "help_command": null,
  "guilds": {
    "GUILDID": {
      "active_groups": [
        "textchannel",
        "voicechannel",
        "greeting"
      ]
    }
  }
}
```

| Column           | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| Command prefix   | Letter that must be written before every command. Example (with '?' as prefix): Command 'test' will be called by '?test'. |
| Case insensitive | Example: if true, command 'test' could also be written 'TEST' (or 'tEst' or 'Test', ...). If false, only 'test' would be valid. |
| Help command     | _Don't change this._                                         |
| Guilds           | Dictionary of all guilds the bot should operate on. Each key is the guild's id. Each value is another dictionary with only one key-value pair: 'active_groups'. |
| Active groups    | List of feature sets that should be active for that guild.   |

> Note: Guild is an synonym for server.



These are the available feature sets:

* textchannel (contains the following)
  * blacklist check
  * link blocker
  * message logger
  * channel clearing
* voicechannel
  * automatic generation of voice channels
  * action logging
* greeting
  * join/leave logging
  * welcoming
  * discharge



If you want to use at lease one feature of each feature set, you'll have to activate that feature set.



##### Explained example

```json
{
  "command_prefix": "!",
  "case_insensitive": true,
  "help_command": null,
  "guilds": {
    "123456789": {
      "active_groups": [
        "textchannel",
        "greeting"
      ]
    }
  }
}
```

In this contains to following information:

* all commands start with '!'
* command detection is case insensitive
* there is one guild
  * it's id is 123456789
  * the active groups are
    * textchannel
    * greeting

So, for that guild, all feature, except those in the voicechannel feature set, can be used, but still need to be configured.
