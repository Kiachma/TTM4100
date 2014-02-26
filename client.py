'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import ReceiveMessageWorker
import json


class Client(object):
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.connection.connect((host, port))
        server_thread = ReceiveMessageWorker(client, self.connection)
        server_thread.daemon = True
        server_thread.start()
        print "Client receive thread :", server_thread.name

    def message_received(self, message, connection):
        response=json.loads(message)
        if response.get('error') is not None:
            print response.get('error')
        elif response.get('response') == 'login':
            print 'Welcome ' + response.get('username')
            for message in response.get('messages'):
                print message
        elif response.get('response') == 'logout':
            print 'Goodbye ' + response.get('username')
        elif response.get('response') == 'message':
            print response.get('message')

    def connection_closed(self, connection):
        connection.close()

    def send(self, data):

        if data.startswith("login"):
            data = {'request': 'login', 'username': data.replace('login ', '')}
        elif data.startswith("logout"):
            data = {'request': 'logout'}
        else:
            data = {'request': 'message', 'message': data}
        self.connection.sendall(json.dumps(data))


    def force_disconnect(self):
        self.connection.close()


if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9999)

    while True:
        message = raw_input('>> \r\n')
        client.send(message)
        if message == '/quit':
            break
    client.force_disconnect()