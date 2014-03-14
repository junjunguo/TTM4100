'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import *
from time import gmtime, strftime
#test 2

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
        self.connection.sendall(data)

    def force_disconnect(self):
        self.connection.close()
        print "connection closed!"

name = "Ole"

if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9988)
    on = True
    while(on):
        r = raw_input(name+': ')
        if r == 'logut':
            on = False
        tid = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        client.send(name+' said @ '+tid+' : '+r)
client.force_disconnect()
