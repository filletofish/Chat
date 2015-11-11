__author__ = 'filletofish'

from queue import Queue
import socket
import os
import threading

server_address = './uds_socket'
number_of_working_threads = 5
#Dictionary for keeping current connections
dict_of_current_connections = {}


#TODO: handle conflict of names (both clients choose the same name)
#TODO: auto updating chat (how??)

# A revised version of our thread class:
class ClientThread(threading.Thread):
# Note that we do not override Thread's __init__ method.
# The Queue module makes this not necessary.

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        # Have our thread serve "forever":
        while True:
            # Get a client out of the queue
            
            #client = clientPool.get()
            client = self.connection

            # Check if we actually have an actual client in the client variable:
            if client != None:
                try:
                    print('SERVER:  connection from', client)
                    name = str(client.recv(1024))[1:]
                    print('SERVER: ' + name + ' has joined the chat')
                    dict_of_current_connections[name] = connection
                    # Receive the data in small chunks and retransmit it
                    while True:
                        data = client.recv(1024)
                        print ('SERVER:  received', data)

                        if str(data) == "b'0'":
                            print('SERVER: Client ' + name + ' disconnected')
                            break
                        elif str(data) == "b'1'":
                            print('SERVER: Client ' + name + ' asks for dict of current connections')
                            ctn = dict_of_current_connections.get(name)
                            ctn.sendall(dict_of_current_connections.keys().__str__()[10:-1].encode())
                        elif data:
                            print ('SERVER:  sending data back to the client')
                            data = (name + ': ' + str(data)[1:]).encode()
                            for ctn in dict_of_current_connections.values():
                                ctn.sendall(data)

                        else:
                            print ('SERVER: no more data from client')
                            break

                finally:
                    # Clean up the connection
                    print('closing' + name)
                    del dict_of_current_connections[name]
                    #print('deleted: ' + dict_of_current_connections.pop(name))
                    print('rest:')
                    print(dict_of_current_connections.keys())
                    client.close()




# Create our Queue:
clientPool = Queue(0)

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
sock.listen(number_of_working_threads)


# Start two threads:
#for x in range(number_of_working_threads):
    #ClientThread().start()



while True:
    # Wait for a connection
    print ('SERVER:  waiting for a connection')
    connection, client_address = sock.accept()
    #clientPool.put(connection)
    ClientThread(connection).start()







