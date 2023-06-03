import json
import re


with open('data.json', 'r') as f:
        data = json.load(f)

def find_persons_by_location_and_date(location, date):
    # this function returns a list of the people who visited a location on a particular date
    # if invalid name or person is given the function returns empty list.
    visitedList = []
    for element in data:
        if element["location"] == location:
            for person in element["persons"]:
                if date in person["dates"]:
                    # I use some regex here because I noticed in the data file multiple names are sometimes stored in one key.
                    # For example, "Brandon \"Bran\" Stark"
                    # Hence I use some regex to split up the names if there are more than one name in a key.
                    names = re.split(r'["\\/]+', person["person"])
                    names = [name.strip() for name in names if name.strip()]
                    visitedList.extend(names)
    return visitedList

def find_locations_by_person_and_date(person, date):
    # Returns all the locations visited by someone on a particular date.
    visited_locations = []
    for locations in data:
        for people in locations['persons']:
            if people['person'] == person and date in people['dates']:
                visited_locations.append(locations['location'])
    return visited_locations

def find_close_contacts(person, date):
    # Finds all the close contacts of a person.
    # This function utilizes the previous functions by finding all locations visited by a person and then 
    # Finding all the people that also visited those locations on the same date.
    close_contacts = []
    visited_locations = find_locations_by_person_and_date(person, date)

    for loc in visited_locations:
        persons_on_date = find_persons_by_location_and_date(loc, date)
        close_contacts.extend([p for p in persons_on_date if p != person])

    return close_contacts

def lambda_handler(event, context):
    # This is the lambda handler function.
    try:

        # When using API Gateway, the payload you send in the request body is contained within the event["body"] key as a string.
        # Hence to get the parameters you must retrieve it from the event body.
        body = json.loads(event["body"])
        function_name = body.get('function')
        params = body.get('params', {})

        # Executes the function according to the function name.
        if function_name == 'find_persons_by_location_and_date':
            location = params.get('location')
            date = params.get('date')
            result = find_persons_by_location_and_date(location, date)
        elif function_name == 'find_locations_by_person_and_date':
            person = params.get('person')
            date = params.get('date')
            result = find_locations_by_person_and_date(person, date)
        elif function_name == 'find_close_contacts':
            person = params.get('person')
            date = params.get('date')
            result = find_close_contacts(person, date)
        else:
            # Error handling if an invalid function name is given.
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Invalid function name provided.'}),
                'isBase64Encoded': False
            }
        # Return the information as an object back.
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result),
            'isBase64Encoded': False
        }
    except Exception as error:
        # This exception is used to catch any errors on the AWS server side & provide more details
        # so it can be easier to debug errors.
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(error)
            }),
            'isBase64Encoded': False
        }




