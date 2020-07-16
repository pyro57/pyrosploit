#!/usr/bin/python3
import pyrosploit
def start_handler():
    attacker = pyrosploit.get_attacker_info()
    handler = pyrosploit.get_server_info(attacker, 'handler')
    handler.start()

if __name__ == '__main__':
    start_handler()

