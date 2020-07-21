# pyrosploit
# TODO
1. encrypt communications between pyterpreter server and client using pub/priv key encryption
2. create a setup script to install what we need and generate the key pair for above communication
3. break into a library file and main script file to make it easier to read
4. Finish pytruder scripts and one-liners
5. add more built in commands to pyterpreter to make it more useful
6. multithread/process it to allow backgrounding of interaction with the shell
7. facilitate multiple shell communcations at the same time using above threading/processing
8. create documentation for contributing commands for pyterpreter/pyrosploit
9. create download cradle one line generator

# Installation
You will need the following python libraries installed: termcolor
after that for now that's pretty much it, once I get the encrpytion part done you'll need to generate the keys to use, which I'll cover here when I get that finished.

# Usage
1. run `python pyrosploit`
2. handler_setup
3. stager_setup
4. pyterpreter_generate
5. stager_start
6. handler_start
running the commands in this order will get you rocking and rolling, basically you'll have a webpage at http://$attacker.ip:stager.port/pyterpreter.py.  The idea is you'll have code execution on a server and you want a better shell that persists but leaves as little trace as possible.  So what you do is create some kind of scheduled task, or cron job, that uses python (powershell eventually maybe) to run this code, and only run it in memory so nothing is dumped to a file.

NOTE: for the time being the shell is a bit finacky and cd doesn't work.


LICENSE:
I'm just gonna call this the pyrolicense.  Do with this project what you will, it is intended to be used by security researches and penetration testers on Networks they have permission to attack.  If you use this tool for illegal actions I can not be held responsible for it.  If you want to take this code and make it your own you may do so, just credit me somewhere in it.
