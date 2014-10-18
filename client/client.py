'''
Created on 15.06.2014

@author: hontonoroger
'''

from gui import GUI
from medium import *
from connection import ServerConnection
from os.path import sys

class Client():
    
    def __init__(self):
        self._server_conn = ServerConnection()
        self._server_media = None
        # TODO: better argument handling
        if len(sys.argv) > 1 and sys.argv[1] == 'console':
            self._server_media = self.get_server_media()
        else:
            self.gui = GUI(self)
        

    def get_server_media(self):
        return self._server_media
    
    def refresh_server_media(self):
        self._server_media = Media().from_json(self._server_conn.get_content().decode())

if __name__ == '__main__':
    client = Client()
    print(client._server_media)
    
# TODO: Teardown: server_conn.close())