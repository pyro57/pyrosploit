#!/bin/python3
import os

def check_root():
    if os.getuid != 0:
        exit("You must run the install as root")
    else:
        return True


def install_dendencies():
    print("installing python-rsa for encryption...")
    os.system('pip install rsa')
    print("installing termcolor")
    os.system('pip install termcolor')


def makekeys():
    import rsa
    (pubkey, privkey) = rsa.newkeys(4096, poolsize=4)
    with open('privkey', 'w') as f:
        f.write(privkey)
    with open('pubkey', 'w') as f:
        f.write(pubkey)


def main():
    if check_root == True:
        install_dendencies()
        makekeys()
        print("Setup complete, happy hunting!")

if __name__ == "__main__":
    main()
