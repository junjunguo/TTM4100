'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import *
from time import gmtime, strftime
import json
import sys

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print self.connection

    def start(self, host, port):
        self.connection.connect((host, port))
        messageThread = ReceiveMessageWorker(client, self.connection)
        messageThread.daemon = True
        messageThread.start()
        print "MessageWorker:", messageThread.name

    def message_received(self, message, connection):
        json_object = json.loads(message)
        if (json_object.get('response') == 'message'):
            if 'message' in json_object:
                print json_object.get('message')
            elif 'error' in json_object:
                print json_object.get('error')

        if (json_object.get('response') == 'logout'):
            if (json_object.get('error') is None):
                print "Logged out!"
            else:    
                print json_object.get('error')

        if (json_object.get('response') == 'login'):
            print "Username:", json_object.get('username')
            if (json_object.get('error') is not None):
                print json_object.get('error')

    def send(self, data):
        if (data.startswith("login")):
            request = {
                'request': 'login',
                'username': data[6:]
            }
        elif (data.startswith('logout')):
            request = {
                'request': 'logout'
            }
        else:
            tid = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            request = {
                'request': 'message',
                'message': ' said @ ' + tid + ' : ' + data
            }
        self.connection.sendall(json.dumps(request))

    def connection_closed(self, connection):
        connection.close()
        print "Connection: ", connection, " closed!"

    def force_disconnect(self):
        self.connection.close()
        print "connection closed!"

#print __name__
if __name__ == "__main__":
    client = Client()
    HOST = 'localhost'
    PORT = 9000
    client.start(HOST, PORT)
    sys.stderr.write("\x1b[2J\x1b[H")
    print """Login required, please write 'login <username>'.
The username must only contain alphanumerical characters and underscores.

To log out, please write 'logout'.
To exit the client, please write 'exit'.
"""
    on = True
    while(on):
        raw = raw_input()
        if raw == 'exit':
            on = False
            client.send('logout')
            print "Client off"
        else:
            client.send(raw) 
