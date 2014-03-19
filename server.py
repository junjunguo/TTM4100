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
                reply, clientname = self.login(json_object)
                print reply, clientname #'line 42'
                if('message' in reply) and ('logged in!' in reply['message']):
                    clients.append(self)
                    print 'clients.append self'
                # send to the client
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
                if (self in clients):
                    reply = {
                        'response': 'logout',
                        'username': clientname
                    }
                    clients.remove(self)
                    onlinenames.remove(clientname)
                    on = False
                else:
                    thereply = {
                        'response': 'logout',
                        'error': 'Not logged in!',
                        'username': clientname
                    }
                    self.send(json.dumps(thereply))
            else:
                if data:
                    print data 
                else:
                    print 'Client disconnected!'
                    on = False
                    onlinenames.remove(clientname)
            #send response to all clients
            if reply:
                for client in clients:
                    client.send(json.dumps(reply))

    def send (self, data):
        self.connection.sendall(data)

    def logout(self, json_object):
        
        
    def login(self, json_object):
        username = json_object.get('username')
        clientname = ''
        if self.isValidName(username):
            if username not in onlinenames:
                onlinenames.append(username)
                clientname = username
                print 'clientname: ', clientname
                print 'onlinenames: ', onlinenames
                reply = {
                    'response': 'message',
                    'message': username + ' logged in!'
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
