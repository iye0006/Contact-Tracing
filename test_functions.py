import unittest
from app import find_persons_by_location_and_date, find_locations_by_person_and_date, find_close_contacts

# Tests if the python functions work correctly and tests some corner cases.
class TestContactTracing(unittest.TestCase):

    def test_find_persons_by_location_and_date(self):
        location = "Asshai"
        date = "2021-02-01T00:00:00.000Z"
        expected = ['Bronn', 'Jon Snow', 'Sansa Stark']
        self.assertEqual(find_persons_by_location_and_date(
            location, date), expected)

    def test_find_locations_by_person_and_date(self):
        person = "Jon Snow"
        date = "2021-02-09T00:00:00.000Z"
        expected = ['Lys', 'Moat Cailin', 'The Golden Tooth']
        self.assertEqual(find_locations_by_person_and_date(
            person, date), expected)

    def test_find_close_contacts(self):
        person = "Jon Snow"
        date = "2021-02-09T00:00:00.000Z"
        expected = ['Davos Seaworth', 'Ramsay Bolton', 'Tywin Lannister', 'Varys', 'Brandon', 'Bran', 'Stark', 'Theon Greyjoy', 'Tyrion Lannister', 'Viserys Targaryen',
                    'Ygritte']
        self.assertEqual(find_close_contacts(person, date), expected)
    # Tests name that doesn't exist
    def test_error_handling(self):
        person = "Jon Sndsfsdfsow"
        date = "2021-02-09T00:00:00.000Z"
        expected = []
        self.assertEqual(find_close_contacts(person, date), expected)
    #Tests invalid date
    def test_error_handling2(self):
        person = "Jon Sndsfsdfsow"
        date = "2021-02-09T00:00:sdfsfs00.000Z"
        expected = []
        self.assertEqual(find_locations_by_person_and_date(person, date), expected)


if __name__ == '__main__':
    unittest.main()
