'''
Created on 19.06.2014

@author: hontonoroger
'''
import socket
import configparser

class ServerConnection:
    '''
    classdocs
    '''

    def __init__(self, hostname='', port=0):
        '''
        Constructor
        '''
        config = configparser.ConfigParser()
        config.read('client.ini')
        
        if hostname == '':
            hostname = config['default']['hostname']
        if port == 0:
            port = int(config['default']['port'])
        self.connect_to(hostname, port)
        
    def connect_to(self, hostname, port):
        self.connection = socket.create_connection((hostname, port))
        
    def close(self):
        self.connection.close()
        
    def get_content(self):
        self.connection.send('get content'.encode())
        return self.connection.recv(1024)