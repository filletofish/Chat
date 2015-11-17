__author__ = 'filletofish'

import socket
import sys


EOF_SPECIFIER = '$$' #using my eof to recognize packets

def sendmsg (sock, str):
    #my end of string
    str += EOF_SPECIFIER
    sock.sendall(str.encode())


def getmsg(sock = socket):
    data =''
    while True:
        new_data = str(sock.recv(1024).decode("utf-8"))
        if new_data == '':
            break
        data += new_data
        while EOF_SPECIFIER in data:
            x = data.find(EOF_SPECIFIER)
            msg = data [:x] + '\''
            data = data[x + 2:]
            print(msg)

try:
    print("Welcome to chat!")
    print("1 - to connect")
    print("0 - to quit")
    while True:

        entry = input()
        if entry == '0':
            break
        elif entry == 'help':
            print("1 - to connect")
            print("0 - to quit")
            continue
        elif entry != '1':
            continue


        try:
            # Create a UDS socket
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            # Connect the socket to the port where the server is listening
            server_address = './uds_socket'
            sock.connect(server_address)
            print ('connecting to %s' % server_address)

        except socket.error as msg:
            print(msg)
            sys.exit(1)
        print('Enter your name:')
        #Sending name
        sock.sendall(input().encode())
        #Turning on timeout
        sock.settimeout(0.5)

        print("0 - to logout")
        print('1 - to get list of connected users')
        while True:
            try:
                getmsg(sock)
            except socket.error as msg:
                pass

            print("Enter your message or just press Enter to get one")

            entry = input()

            if entry == '':
                continue
            elif entry == '0':
                sock.sendall('0'+EOF_SPECIFIER.encode())
                print('CLIENT: disconnecting from chat')
                sock.close()
                break
            elif entry == '1':
                sock.sendall('1'+EOF_SPECIFIER.encode())
                entry = sock.recv(1024)
                print('Connected:')
                print(entry.decode("utf-8"))
            elif entry == 'help':
                print('0 - to logout')
                print('1 - to get list of connected users')
            else:
                sendmsg(sock, entry)

finally:
        print("Quited")


# old version
# def getmsg(sock = socket):
#     data = sock.recv(1024)
#     if data:
#         data = str(data.decode("utf-8"))
#         for a in data.split('$$\''):
#             if (a != ""):
#                 a+= "\'"
#                 print(a)
