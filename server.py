'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''

import SocketServer
import json

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
        #Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        print 'Client connected @' + self.ip + ':' + str(self.port)
        # Wait for data from the client
        on = True
        clientname = ''
        reply = ''
        while (on):
            # Check if the data exists
            data = self.connection.recv(1024).strip()
            print data
            # (recv could have returned due to a disconnect)
            # decoding to json object
            json_object = json.loads(data)

            if json_object.get('request') == 'login':
                if (self in clients):
                    thereply = {
                        'response': 'message',
                        'message':  'logout befor you login with another name!'
                        }
                    self.send(json.dumps(thereply))
                    reply = ''
                else:
                    reply, clientname = self.login(json_object)
                    print reply 
                    if (clientname is not ''):
                        clients.append(self)
                        print "Client appended!"
                        print "Online names: ", onlinenames
                    else:
                        self.send(json.dumps(reply))

            elif json_object.get('request') == 'message':
                if self in clients:
                    reply = {
                        'response': 'message',
                        'message': clientname + json_object.get('message')
                    }
                else:
                    reply = {
                        'response': 'message',
                        'error': 'You are not logged in!',
                        }
                    self.send(json.dumps(reply))

            elif json_object.get('request') == 'logout':
                reply, clientname = self.logout(json_object)
                print reply
                if (clientname is not '' or None):
                    clients.remove(self)
                    print "Client removed!"
                    print "Onlinenames: ", onlinenames
                else:
                    self.send(json.dumps(reply))

            else:
                if data:
                    print data 
                else:
                    print 'Client disconnected!'
                    on = False

    def send (self, data):
        self.connection.sendall(data)

    def logout (self, json_object):
        username = json_object.get('username')
        clientname = ''
        if (username in onlinenames):
            reply = {
                'response': 'logout',
                'username': username
            }
            onlinenames.remove(username)
            print "Onlinename removed!"
            clientname = username
        else:
            reply = {
                'response': 'logout',
                'error': 'Not logged in!',
                'username': username
            }
        return reply, clientname

    def login (self, json_object):
        username = json_object.get('username')
        clientname = ''
        if self.isValidName(username):
            if username not in onlinenames:
                onlinenames.append(username)
                clientname = username
                print "Onlinename appended!"
                reply = {
                    'response': 'login',
                    'username': username
                }
            else:
                reply = {
                    'response': 'login',
                    'error': 'Name already taken!',
                    'username': username
                }
        else:
            reply = {
                'response': 'login',
                'error': 'Invalid username!',
                'username': username
            }
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
    PORT = 9988

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), CLientHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
