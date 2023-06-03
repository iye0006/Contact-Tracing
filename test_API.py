import requests
import unittest

api_url = "https://pae4znlv6b.execute-api.us-east-1.amazonaws.com/prod/testresource" 

# Tests if the API functions correctly with some different inputs and some error handling as well.
class TestRequests(unittest.TestCase):
    def test_find_persons_by_location_and_date(self):
        payload1 = {
            "function": "find_persons_by_location_and_date",
            "params": {
                "location": "Asshai",
                "date": "2021-02-01T00:00:00.000Z"
            }
        }
        response1 = requests.post(api_url, json=payload1)
        expected = ['Bronn', 'Jon Snow', 'Sansa Stark']
        self.assertEqual(response1.json(), expected)

    def test_find_locations_by_person_and_date(self):
        payload2 = {
            "function": "find_locations_by_person_and_date",
            "params": {
                "person": "Jon Snow",
                "date": "2021-02-09T00:00:00.000Z"
            }
        }   
        response2 = requests.post(api_url, json=payload2)
        expected = ['Lys', 'Moat Cailin', 'The Golden Tooth']
        self.assertEqual(response2.json(), expected)

    def test_find_close_contacts(self):
        payload3 = {
            "function": "find_close_contacts",
            "params": {
                "person": "Jon Snow",
                "date": "2021-02-09T00:00:00.000Z"
            }
        }
        expected = ['Davos Seaworth', 'Ramsay Bolton', 'Tywin Lannister', 
                    'Varys', 'Brandon', 'Bran', 'Stark', 'Theon Greyjoy', 
                    'Tyrion Lannister', 'Viserys Targaryen', 'Ygritte']
        response3 = requests.post(api_url, json=payload3)
        self.assertEqual(response3.json(), expected)
    
    def test_error_handling(self):
        payload4 = {
            "function": "find_close_contacts",
            "params": {
                "person": "Jon Snoooow",
                "date": "2021-02-09T00:00:00.000Z"
            }
        }
        expected = []
        response4 = requests.post(api_url, json=payload4)
        self.assertEqual(response4.json(), expected)
        
    def test_function_error(self):
        # Tests error handling if invalid function name is given.
        payload5 = {
            "function": "error",
            "params": {
                "person": "Jon Snoooow",
                "date": "2021-02-09T00:00:00.000Z"
            }
        }
        expected = {'error': 'Invalid function name provided.'}
        response5 = requests.post(api_url, json=payload5)
        self.assertEqual(response5.json(), expected)

if __name__ == '__main__':
    unittest.main()