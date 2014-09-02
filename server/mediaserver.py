'''
Created on 19.06.2014

@author: hontonoroger
'''

import socket
import logging
import configparser
import database
from medium import Medium, Media
from Crypto.Util.RFC1751 import binary
import os
import shutil
from os.path import sys

logging.getLogger().setLevel(logging.DEBUG)

class MediaServer:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('server.ini')
        
        self.db = database.Database('media.db')

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # TODO: get options from a configuration file
        self._hostname = config['main']['hostname']
        self._port = int(config['main']['port'])

        self.connection.bind((self._hostname, self._port))
        print("Server bound to", self._hostname, self._port)

    def return_content(self):
        """
        Returns a JSON formatted binary string with all available media.
        """
        results = Media(self.db.find_entries())
        #return b"bli, bla, blubb"
        if not results._media:
            logging.debug("Answer is empty.")
            return b'[]'
        else:
            response = results.to_json()
            logging.debug("Answer is: " + response)
            return response.encode() # must be binary encoded


    def run(self):
        self.connection.listen(5)
        print("Server is now listening for new connections.")
        while True:
            client, addr = self.connection.accept()
            request = client.recv(1024)
            logging.debug(request)
            if request == b'get content':
                logging.info("Returning contents of media server to client %s", addr[0])
                client.send(self.return_content())
                
    def start_stream(self, media_id):
        pass
    
    
if __name__ == '__main__':
    server = MediaServer()
    server.run()