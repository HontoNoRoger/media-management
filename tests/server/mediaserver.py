'''
Created on 30.07.2014

@author: hontonoroger
'''
import unittest
import os
from mediaserver import MediaServer
from medium import Medium


class Test(unittest.TestCase):


    def setUp(self):
        self.server = MediaServer()

    def tearDown(self):
        os.remove('media.db')

    def testSaveMedium(self):
        medium = Medium(0,
                        "Film",
                        "Testname des Films XY",
                        "Action",
                        54728,
                        "Beschreibungstext des\nFilms",
                        os.stat("testfile.webm").st_size)
        medium.media_id = self.server.save_medium(medium, "testfile.webm", 'webm')
        self.assertEqual(medium.media_id, 1)
        
        created_file = open('data/Film/Action/' + str(medium.media_id) + '.webm', 'r')
        self.assertTrue(created_file)
        
        created_file.close()
        os.remove('data/Film/Action/' + str(medium.media_id) + '.webm')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSaveMedium']
    unittest.main()