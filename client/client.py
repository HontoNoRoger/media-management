'''
Created on 15.06.2014

@author: hontonoroger
'''

from gui import GUI
from connection import ServerConnection

class Client():
    
    def __init__(self):
        self.gui = GUI()
        self.server_conn = ServerConnection()


if __name__ == '__main__':
    server_connection = ServerConnection()
    print(server_connection.get_content())
#     exit(0) # TODO: only there for test purposes
    client = Client()
    
# TODO: Teardown: server_conn.close())