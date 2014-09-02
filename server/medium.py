'''
Created on 25.06.2014

@author: hontonoroger
'''
import json

class Medium():
    '''
    classdocs
    '''


    def __init__(self, media_id = 0, 
                 media_type = None,
                 name = None,
                 genre = None,
                 length = 0,
                 description = None,
                 size = 0,
                 medium_dict = None):
        '''
        Constructor
        '''
        if medium_dict:
            self.media_id = medium_dict['media_id']
            self.media_type = medium_dict['media_type']
            self.name = medium_dict['name']
            self.genre = medium_dict['genre']
            self.length = medium_dict['length']
            self.description = medium_dict['description']
            self.size = medium_dict['size']
        else:
            self.media_id = media_id
            self.media_type = media_type
            self.name = name
            self.genre = genre
            self.length = length
            self.description = description
            self.size = size
        
    def from_json(self, json_string):
        json_object = json.loads(json_string)
        self.media_id = json_object['media_id']
        self.media_type = json_object['media_type']
        self.name = json_object['name']
        self.genre = json_object['genre']
        self.length = json_object['length']
        self.description = json_object['description']
        self.size = json_object['size']
        return self
    
    def to_json(self):
        json_structure = {'media_id': self.media_id,
                          'media_type': self.media_type,
                          'name': self.name,
                          'genre': self.genre,
                          'length': self.length,
                          'description': self.description,
                          'size': self.size}
        return json.dumps(json_structure)

    def return_dict(self):
        medium_dict = {'media_id': self.media_id,
                          'media_type': self.media_type,
                          'name': self.name,
                          'genre': self.genre,
                          'length': self.length,
                          'description': self.description,
                          'size': self.size}
        return medium_dict

class Media():
    """
    Doc
    """
        
    def __init__(self, mediumlist = None):
        self._media = {}
        
        if mediumlist:
            print('Building new media from:')
            print(mediumlist)
            for medium in mediumlist:
                self.addMedium(Medium(medium_dict=medium))
    
    def addMedium(self, medium):
        self._media[medium.media_id] = medium
    
    def removeMedium(self, medium):
        try:
            del self._media[medium.media_id]
        except TypeError:
            # Might be the case if medium is not a type of Medium
            # but the media_id
            del self.media[medium]
    
    def getMedium(self, media_id):
        return self._media.get(media_id)
    
    def filterMedia(self,
                    media_type = None, 
                    name = None,
                    genre = None,
                    length = None,
                    description = None,
                    size = None):
        pass
    
    def to_json(self):
        json_structure = []
        for medium in self._media.values():
            json_structure.append(medium.return_dict())
        return json.dumps(json_structure)