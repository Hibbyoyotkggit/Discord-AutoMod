## Installation

### Python

At first you'll need to install Python (>= 3.8, but I'd recommend you to choose the newest version) if it isn't already installed. On most Linux-distributions, it probably is.  



You can download Python at [python.org](https://www.python.org/downloads). Choose the right download for your OS and install it. For Linux, you might have to build it form source yourself. [Here](https://tecadmin.net/how-to-install-python-3-9-on-ubuntu-debian-linuxmint/) is an installation guide (should work for 3.8.* _and_ 3.9.*).



### PIP

PIP (**P**ackage **I**ndex for **P**ython) is used to install python packages. Pip is available via APT on ubuntu (and maybe on other distros too).

To install it via APT

```bash
# via apt
sudo apt install python3-pip
# or via apt-get
sudo apt-get install python3-pip
```



For other Linux-distros, Windows (I'm not sure whether it works on MacOS too) you can use the [get-pip.py](https://bootstrap.pypa.io/get-pip.py) script. Simply download and execute it.

Then try to run the following commands in a Terminal (Linux) or a PowerShell (Windows):

```bash
# one of the following should work
pip --version
pip3 --version
python3 -m pip --version # maybe you'll need to use 'python3.8' or 'python3.9' instead of 'python3'
# should display something like
# pip 21.2.1 from /home/bob/.local/lib/python3.9/site-packages/pip (python 3.9)
#                                                                          | this is important and should be >= 3.8
```





### Discord.py

Discord.py is the python library for communicating with [discord's](https://discord.com) API. It can be installed via PIP.

Run (choose the same variant as for the installation of pip):

```bash
# one of the following should work
pip install discord
pip3 install discord
python3 -m pip install discord
```
