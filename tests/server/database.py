'''
Created on 25.06.2014

@author: hontonoroger
'''
import unittest
import os
from database import Database

class Test(unittest.TestCase):

    def setUp(self):
        self.db = Database('test.db')

    def tearDown(self):
        self.db.close()
        os.remove('test.db')

    def testConnection(self):
        self.assertTrue(self.db)
    
    def testAddEntry(self):
        status = self.db.add_entry('Film', 'Analmassaker 3', 'Erotik', 37323 ,
                          'Ein ganz besonderer Film. Er macht betroffen', 1324234243)
        self.assertGreater(status, 0)
        
    def testGetEntry(self):
        self.db._c.execute("insert into media(rowid, media_type, name, genre, length, description, size) values (555, 'Film', 'Testname', 'Action', 742, 'Testbeschreibung', 123456789)")
        result = self.db.get_entry(555)
        self.assertEqual(result, (555, 'Film', 'Testname', 'Action', 742, 'Testbeschreibung', 123456789))
        
    def testRemoveEntry(self):
        self.db._c.execute("insert into media(rowid, media_type, name, genre, length, description, size) values (666, 'Film', 'Testname', 'Action', 742, 'Testbeschreibung', 123456789)")
        self.db.remove_entry(666)
        self.db._c.execute("select * from media where ROWID = ?", (666, ))
        result = self.db._c.fetchone()
        self.assertFalse(result)
        
    def testUpdateEntry(self):
        self.db._c.execute("insert into media(rowid, media_type, name, genre, length, description, size) values (666, 'Film', 'Testname', 'Action', 742, 'Testbeschreibung', 123456789)")
        self.db.update_entry(666, name = 'Changed Name', genre = "Drama", description = "All better now")
        self.db._c.execute("select * from media where ROWID = ?", (666, ))
        result = self.db._c.fetchone()
        self.assertEqual(result, ('Film', 'Changed Name', 'Drama', 742, 'All better now', 123456789))
        
    def testFindEntries(self):
        self.db._c.execute("insert into media(rowid, media_type, name, genre, length, description, size) values (666, 'Film', 'Testname', 'Action', 12345, 'Testbeschreibung', 123456789)")
        self.db._c.execute("insert into media(rowid, media_type, name, genre, length, description, size) values (333, 'Film', 'Best movie ever', 'Doku', 12345, 'All about movies', 47827432)")
        results = self.db.find_entries('Film')
        self.assertCountEqual(results, [
            (666, 'Film', 'Testname', 'Action', 12345, 'Testbeschreibung', 123456789),
            (333, 'Film', 'Best movie ever', 'Doku', 12345, 'All about movies', 47827432)])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConnection']
    unittest.main()