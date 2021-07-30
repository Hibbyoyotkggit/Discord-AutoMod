## Configuration

To get the bot running a few configuration tasks have to done, but most of them can be done with a script.



#### 1. Run configure.py

Change into the Discord-AutoMod directory and run configure.py with:

```bash
python3.8 configure.py
# or
python3.9 configure.py
# or 
python3 configure.py
```

After that, the main configuration stuff is done.



#### 2. Adjust specific config files

##### blacklist

if you have enabled the module 'wordBlacklist' open blacklist.json and add words to the blacklist like this:

```json
{
    "YOURGUILDID": {
    	"blacklist": [
    		"add",
    		"words",
            "here",
            "to",
            "the",
            "list"
    	]
    }
}
```

In the example 'add', 'words', 'here', 'to', 'the' and 'list' are added to the blacklist.
