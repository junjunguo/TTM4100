'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import socket
import SocketServer
import json
import sys

# client list:
clients = []
# list of online names
onlinenames = []
'''
The RequestHandler class for our server.
It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''

class CLientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.connection = self.request
        print self.connection
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        print 'Client connected @' + self.ip + ':' + str(self.port)
        on = True
        clientname = ''
        while (on):
            data = self.connection.recv(4096)
            if data:
                print data
                json_object = json.loads(data)
            #-------------------------------------------------
                if json_object.get('request') == 'login':
            #-------------------------------------------------
                    if (self in clients):
                        reply = {
                            'response': 'message',
                            'message': 'Logout before you login with another name!'
                            }
                        self.send(json.dumps(reply))
                        print reply
                        reply = None
            #------------------------------------------------
                    else:
                        reply, clientname = self.login(json_object)
                        self.send(json.dumps(reply))
                        print reply
                        reply = None
            #-------------------------------------------------
                elif json_object.get('request') == 'message':
                    if (self in clients):
                        reply = {
                            'response': 'message',
                            'message': clientname + json_object.get('message')
                        }
                        print reply
            #-------------------------------------------------
                    else:
                        reply = {
                            'response': 'message',
                            'error': 'You are not logged in!',
                            }
                        self.send(json.dumps(reply))
                        print reply
                        reply = None
            #-------------------------------------------------
                elif json_object.get('request') == 'logout':
                    reply = self.logout(json_object, clientname)
                    self.send(json.dumps(reply))
                    print reply
                    reply = None
            #-------------------------------------------------
                if reply:
                    for client in clients:
                        client.send(json.dumps(reply))
            #-------------------------------------------------
            else:
                on = False
                print "Serving off"

    def send (self, data):
        self.connection.sendall(data)

    #---------------------------------------------------------
    def logout (self, json_object, clientname):
        if (clientname in onlinenames):
            reply = {
                'response': 'logout'
            }
            clients.remove(self)
            onlinenames.remove(clientname)
            print "Onlinenames: ", onlinenames
        else:
            reply = {
                'response': 'logout',
                'error': 'Not logged in!'
            }
        return reply

    #--------------------------------------------------------
    def login (self, json_object):
        username = json_object.get('username')
        clientname = ''
        if self.isValidName(username):
        #---------------------------------- 
            if username not in onlinenames:
                clientname = username
                clients.append(self)
                onlinenames.append(clientname)
                print "Online names: ", onlinenames
                reply = {
                    'response': 'login',
                    'username': username
                }
        #----------------------------------- 
            else:
                reply = {
                    'response': 'login',
                    'error': 'Name already taken!',
                    'username': username
                }
        #---------------------------------------
        else:
            reply = {
                'response': 'login',
                'error': 'Invalid username!',
                'username': username
            }
        #------------------------------------------------------
        return reply, clientname

    def isValidName(self, name):
        validString = "abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if (len(name) < 1):
            return False
        for c in name:
            if (c not in validString):
                return False
        return True

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

#print __name__
if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9000
    server = ThreadedTCPServer((HOST, PORT), CLientHandler)
    sys.stderr.write("\x1b[2J\x1b[H")
    print "Server initialized!"
    server.serve_forever()
