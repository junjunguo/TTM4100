'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer

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
        while (on):
            # Check if the data exists
            data = self.connection.recv(1024).strip()
            self.server.gmessage.append(data)
            # (recv could have returned due to a disconnect)
            logut = data[-5:]
            if logut == 'logut':
                print data
                self.send(data)
                on = False
            else:
                if data:
                    print data 
                    # Return the string in uppercase
                    self.send(data)
                    #self.connection.sendall(gmessage.upper())
                   # gmessage = null
                else:
                    print 'Client disconnected!'
                    on = False
            for message in gmessage:
                self.server.broadcast(message)
                print message
    def send (self, data):
        self.connection.sendall(data.upper())
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    gmessage = []
    clients = {}
    def broadcast(self, message):
        for client in self.clients:
            client.sendall(message)

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9988
    gmessage = 0
    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), CLientHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
