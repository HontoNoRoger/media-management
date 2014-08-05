'''
Created on 19.06.2014

@author: hontonoroger
'''

import socket
import logging
import configparser
import database
from medium import Medium
from Crypto.Util.RFC1751 import binary
import os
import shutil

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
        results = Medium(self.db.find_entries())
        #return b"bli, bla, blubb"
        return binary(results.to_json()) # must be binary encoded


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
    
    def save_medium(self, medium, file, extension):
        """
        Saves the given file with it's medium settings into the database
        and on the file system.
        
        TODO: Automatically get file extension
        """
        
        # Save media entry in database
        medium.media_id = self.db.add_entry(medium.media_type, medium.name,
                                            medium.genre, medium.length,
                                            medium.description, medium.size)
        
        # Make sure the target path exists
        if not os.path.isdir('data'): 
            os.mkdir('data')
        if not os.path.isdir('data/' + medium.media_type): 
            os.mkdir('data/' + medium.media_type)
        if not os.path.isdir('data/' + medium.media_type + '/' + medium.genre): 
            os.mkdir('data/' + medium.media_type + '/' + medium.genre)
            
        #TODO: rename file after it's row ID and save it under
        # data/type/genre/id.ext
        #file_target = open('data/' + medium.media_type + '/' + medium.genre + '/'
        #                  + str(medium.media_id) + '.' + extension, 'w')
        shutil.copyfile(file, 'data/' + medium.media_type + '/' + medium.genre + '/'
                           + str(medium.media_id) + '.' + extension)
        #file_target.write(file.read())
        #file_target.close()
        
        return medium.media_id
    
if __name__ == '__main__':
    server = MediaServer()
    server.run()