'''
Created on 15.06.2014

@author: hontonoroger
'''

from gui import GUI
from connection import ServerConnection
from os.path import sys

class Client():
    
    def __init__(self):
        self.server_conn = ServerConnection()
        if len(sys.argv) > 0 and sys.argv[1] != 'console':
            self.gui = GUI()


if __name__ == '__main__':
    #server_connection = ServerConnection()
#     exit(0) # TODO: only there for test purposes
    client = Client()
    print(client.server_conn.get_content())
    
# TODO: Teardown: server_conn.close())