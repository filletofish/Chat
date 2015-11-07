__author__ = 'filletofish'

import socket
import sys

def sendmsg (sock, str = str):
    str += '$$'
    sock.sendall(str.encode())

def getmsg(sock = socket):
    data = sock.recv(1024)
    if data:
        data = str(data.decode("utf-8"))
        for a in data.split('$$\''):
            if (a != ""):
                a+= "\'"
                print(a)


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
        sock.settimeout(0.5)

        print("0 - to logout")
        print('1 - to get list of connected users')
        while True:
            try:
                getmsg(sock)
            except socket.error as msg:
                pass
                print('..')

            print("Enter your message or just press Enter to get one")
            data = input()

            if data == '':
                continue
            elif data == '0':
                sock.sendall('0'.encode())
                print('CLIENT: disconnecting from chat')
                sock.close()
                break
            elif data == '1':
                sock.sendall('1'.encode())
                data = sock.recv(1024)
                print('Connected:')
                print(data.decode("utf-8"))
            elif data == 'help':
                print('0 - to logout')
                print('1 - to get list of connected users')
            else:
                sendmsg(sock, data)

finally:
        print("Quited")