__author__ = 'filletofish'

import socket
import os
import threading


LISTENERS = 5
EOF_SPECIFIER = '$$'

server_address = './uds_socket'
#Dictionary for keeping current connections
current_connections = {}


#TODO: handle conflict of names (both clients choose the same name)
#TODO: auto updating chat (how??)

# Threading lock for sync our current_connections
lock = threading.Lock()

# A revised version of our thread class:
class ClientThread(threading.Thread):


    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        global lock

        # Have our thread serve "forever":
        while True:
            client = self.connection

            # Check if we actually have an actual client in the client variable:
            if client != None:
                try:
                    print('SERVER:  connection from', client)
                    name = str(client.recv(1024))[1:]
                    print('SERVER: ' + name + ' has joined the chat')

                    #Locking
                    lock.acquire()
                    try:
                        current_connections[name] = connection
                    finally:
                        lock.release()

                    # Receive the data in small chunks and retransmit it
                    data =''
                    msg = ''
                    while True:

                        while True:
                            new_data = client.recv(1024)
                            data += str(new_data)[1:] #deleting 'b'
                            if EOF_SPECIFIER in data:
                                x = data.find(EOF_SPECIFIER)
                                msg = data [1:x]
                                data = data[x + 3:]
                                print (msg)
                                print (data)
                                break

                        print ('SERVER:  received', msg)

                        if str(msg) == '0':
                            print('SERVER: Client ' + name + ' disconnected')
                            break
                        elif str(msg) == '1':
                            print('SERVER: Client ' + name + ' asks for dict of current connections')
                            ctn = current_connections.get(name)
                            ctn.sendall(current_connections.keys().__str__()[10:-1].encode())
                        elif msg:
                            print ('SERVER:  sending data back to the client')
                            msg = (name + ': ' + '\'' + msg + EOF_SPECIFIER).encode()

                            # Locking
                            lock.acquire()
                            try:
                                for ctn in current_connections.values():
                                    ctn.sendall(msg)
                            finally:
                                lock.release()

                        else:
                            print ('SERVER: no more data from client')
                            break

                finally:
                    # Clean up the connection
                    print('closing' + name)
                    # Locking
                    lock.acquire()
                    try:
                        del current_connections[name]
                    finally:
                        lock.acquire()

                    print('rest:')
                    print(current_connections.keys())
                    client.close()



# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
print ('SERVER:  starting up on %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(LISTENERS)


while True:
    # Wait for a connection
    print ('SERVER:  waiting for a connection')
    connection, client_address = sock.accept()
    ClientThread(connection).start()