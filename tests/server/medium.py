'''
Created on 30.07.2014

@author: hontonoroger
'''
import unittest
from medium import Medium, Media
import json

class Test(unittest.TestCase):


    def testMediumFromJSON(self):
        json_string = '{"media_id": 555, "media_type": "Film", "name": "Testname", "genre": "Action", "length": 742, "description": "Testbeschreibung", "size": 123456789}'
        expected_result = Medium(555, 'Film', 'Testname', 'Action', 742, 'Testbeschreibung', 123456789)
        result = Medium().from_json(json_string)
        self.assertDictEqual(result.return_dict(), expected_result.return_dict())
    
    def testMediumToJSON(self):
        medium = Medium(555, 'Film', 'Testname', 'Action', 742, 'Testbeschreibung', 123456789)
        expected_result = '{"media_id": 555, "media_type": "Film", "name": "Testname", "genre": "Action", "length": 742, "description": "Testbeschreibung", "size": 123456789}'
        self.assertDictEqual(json.loads(medium.to_json()), json.loads(expected_result))
    
    def testMediaToJSON(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFromJSON']
    unittest.main()