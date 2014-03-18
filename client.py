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
        messageThread.start()
        print "MessageWorker:", messageThread.name

    def message_received(self,message,connection):
        json_object = json.loads(message)
        if (json_object.get('response') == 'message'):
            if 'message' in json_object:
                print json_object.get('message')
            elif 'error' in json_object:
                print json_object.get('error')
        if (json_object.get('response') == 'logout'):
            if 'username' in json_object:
                print json_object.get('username'),json_object.get('username')
            else:
                print json_object.get('username'), json_object.get('error')

        if (json_object.get('response') == 'login'):
            print json_object.get('username'), json_object.get('error')

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
                'message': ' said @ ' + tid + ' : ' + data
            }
        # encode to python before sending
        self.connection.sendall(json.dumps(request))

    def force_disconnect(self):
        self.connection.close()
        print "connection closed!"

#print __name__
if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9988)
    print "Login required, please write 'login <username>'."
    print "The username must only contain alphanumerical characters and underscores."
    on = True
    while(on):
        raw = raw_input(': ')
        if raw == 'logout':
            on = False
        client.send(raw)
client.force_disconnect()        
