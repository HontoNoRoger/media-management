#!/usr/bin/python
'''
Created on 10.08.2014

@author: hontonoroger
'''
import medium
import os
import shutil
import configparser
import database
import glob
from medium import Medium

        
def save_medium(medium, file, extension):
    """
    Saves the given file with it's medium settings into the database
    and on the file system.
    
    TODO: Automatically get file extension
    """      
    db = database.Database('media.db')
    
    # Save media entry in database
    medium.media_id = db.add_entry(medium.media_type, medium.name,
                                        medium.genre, medium.length,
                                        medium.size, medium.description)
    
    # Make sure the target path exists
    if not os.path.isdir('data'): 
        os.mkdir('data')
    if not os.path.isdir('data/' + medium.media_type): 
        os.mkdir('data/' + medium.media_type)
    if not os.path.isdir('data/' + medium.media_type + '/' + medium.genre): 
        os.mkdir('data/' + medium.media_type + '/' + medium.genre)
        
    # rename file after it's row ID and save it under
    # data/type/genre/id.ext
    #file_target = open('data/' + medium.media_type + '/' + medium.genre + '/'
    #                  + str(medium.media_id) + '.' + extension, 'w')
    if medium.media_id > 0:
        shutil.copyfile(file, 'data/' + medium.media_type + '/' + medium.genre + '/'
                       + str(medium.media_id) + '.' + extension)
    
    return medium.media_id
        
if __name__ == '__main__':
    if not os.path.isdir('import'):
        exit("No import folder present")
        
    mediumconfig = configparser.ConfigParser()
    
    for file in glob.glob('import/*.medium'):
        
        print('Importing medium ' + file)
        mediumconfig.read(file)
        newmedium = Medium(media_type = mediumconfig['info']['media_type'],
                 name = mediumconfig['info']['name'],
                 genre = mediumconfig['info']['genre'],
                 length = mediumconfig['info']['length'],
                 size = os.path.getsize('import/' + mediumconfig['file']['filename']),
                 description = mediumconfig['info']['description'])
        returncode = save_medium(newmedium, 'import/' + mediumconfig['file']['filename'], mediumconfig['file']['extension'])
        
        if returncode == 0:
            print('Could not import medium ' + file)
        else:
            os.rename(file, file + '.old')
            print('Medium ' + file + ' imported')
        #save_medium()
    