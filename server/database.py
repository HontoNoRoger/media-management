'''
Created on 19.06.2014

@author: hontonoroger
'''

import sqlite3

class Database:
    '''
    classdocs
    '''

    def __init__(self, dbname):
        '''
        Constructor
        '''
        self._db = sqlite3.connect(dbname)
        self._c = self._db.cursor()
        self._c.execute("create table if not exists media (media_type TEXT, name TEXT, genre TEXT, length INT, description TEXT, size BIGINT)")

    def add_entry(self, media_type, name, genre, length, description, size):
        status = self._c.execute("insert into media values (?, ?, ?, ?, ?, ?)",
                                 (media_type, name, genre, length, description, size))
        
        if status.lastrowid != None:
            self._db.commit()
            return status.lastrowid
        else:
            self._db.rollback()
            return 0
        

    def remove_entry(self, media_id):
        self._c.execute("delete from media where ROWID = ?", (media_id, ))
        self._db.commit()

    def get_entry(self, media_id):
        # Execute statement expects a tuple, list or dictionary as
        # variable parameter so we're using a tuple with an empty field here.
        self._c.execute("select ROWID, * from media where ROWID = ?", (media_id, ))
        return self._c.fetchone()

    def update_entry(self, media_id, media_type = None, name = None, genre = None, length = None, description = None, size = None):
        """
        Updates an entry based on given parameters.
        
        TODO: only use one query
        """
        last_row_id = None
        
        if (media_type):
            last_row_id = self._c.execute("update media set media_type = ? where ROWID = ?", (media_type, media_id))
        if (name):
            last_row_id = self._c.execute("update media set name = ? where ROWID = ?", (name, media_id))
        if (genre):
            last_row_id = self._c.execute("update media set genre = ? where ROWID = ?", (genre, media_id))
        if (length):
            last_row_id = self._c.execute("update media set length = ? where ROWID = ?", (length, media_id))
        if (description):
           last_row_id =  self._c.execute("update media set description = ? where ROWID = ?", (description, media_id))
        if (size):
            last_row_id = self._c.execute("update media set size = ? where ROWID = ?", (size, media_id))
            
        return last_row_id
    
    def find_entries(self, media_type = None, name = None, genre = None, length = None, description = None, size = None):
        """
        Gets all media with matching …
        """
        query = "select ROWID, * from media "
        where_clause = []
        if (media_type):
            where_clause.append("media_type = '" + media_type + "'")
        if (name):
            where_clause.append("name = '" + name + "'")
        if (genre):
            where_clause.append("genre = '" + genre + "'")
        if (length):
            where_clause.append("length = '" + length + "'")
        if (description):
            where_clause.append("description = '" + description + "'")
        if (size):
            where_clause.append("size = '" + size + "'")
        
        where_size = len(where_clause)
        if (where_size > 0):
            query += 'where '
        for statement in where_clause:
            query += statement
            where_size -= 1
            if where_size > 0:
                query += " AND "
        print(query)
        self._c.execute(query)
        
        media_list = []
        for medium_tuple in self._c.fetchall():
            media_list.append(self._tuple_to_dict(medium_tuple))
        return media_list
        
    def get_next_available_rowid(self):
        self._c.execute("SELECT * FROM SQLITE_SEQUENCE WHERE name='media'")
        return self._c.fetchone().seq + 1 
    
    def close(self):
        self._db.close()
        
    def _tuple_to_dict(self, medium_tuple):
        '''
        Converts a database tuple to a dictionary.
        '''
        medium_dict = {}
        medium_dict['media_id'] = medium_tuple[0]
        medium_dict['media_type'] = medium_tuple[1]
        medium_dict['name'] = medium_tuple[2]
        medium_dict['genre'] = medium_tuple[3]
        medium_dict['length'] = medium_tuple[4]
        medium_dict['description'] = medium_tuple[5]
        medium_dict['size'] = medium_tuple[6]
        return medium_dict