'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import *
from time import gmtime, strftime
import json

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.connection.connect((host, port))
        messageThread = ReceiveMessageWorker(client, self.connection)
        messageThread.daemeon = True
        messageThread.start()
        print "MessageWorker:",messageThread.name

    def message_received(self,message,connection):
        print message

    def connection_closed(self, connection):
        connection.close()
        print "Connection: "+connection+" closed!"

    def send(self, data):
        if ( data.startswith("login")):
            request = {
                'request': 'login',
                'username': data[6:]
            }
        elif ( data.startswith("logout")):
            request = {
                'request': 'logout'
            }
        else:
            tid = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            request = {
                'request': 'message',
                'message': ' said @ '+tid+' : '+data
            }
        # encode to python's type before sending
        self.connection.sendall(json.dumps(request))

    def force_disconnect(self):
        self.connection.close()
        print "connection closed!"


if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9988)
    print "login required, please write 'login <username>'"
    print "only contain alphanumerical characters and underscores"
    on = True
    while(on):
        r = raw_input(': ')
        if r == 'logout':
            on = False
        client.send(r)
client.force_disconnect()        
