#!/usr/bin/python3
import pyrosploit
import time

attacker = pyrosploit.get_attacker_info()
stager = pyrosploit.get_server_info(attacker, 'http')
stager.start()
time.sleep(1)
input('press enter to shutdown server and exit')
stager.stop()

