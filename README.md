# Contact Tracing API

This project provides a simple API to perform contact tracing tasks using AWS Lambda and API Gateway. The API consists of three main functions which were written in python:

1. `find_persons_by_location_and_date(location, date)` :  Returns a list of persons at a given location on a specific date.
2. `find_locations_by_person_and_date(person, date)` : Returns a list of locations visited by a specific person on a given date.
3. `find_close_contacts(person, date)` : Returns a list of close contacts for a specific person on a given date.

api_url = "https://pae4znlv6b.execute-api.us-east-1.amazonaws.com/prod/testresource" 

(By the time I realized I was using the wrong region I was near the completion of the task. For this task, I don't think it makes too much of a difference however)


## Overview of Project architecture

1. Python functions are loaded in a zip file to AWS Lambda.
2. AWS Gateway REST API is connected with the Lambda function and configured so that incoming requests are processed to the Lambda function
3. API is deployed and an endpoint URL can be used to send requests (examples shown later)

## Project Files

1. app.py  - The main Python script that containts the Lambda event handler and all the contact tracing functions
2. test_functions.py - Contains tests for the contact tracing function to check if the functions work.
3. test_API.py - tests if the API endpoint works by testing different requests.
4. data.json - The json file with contact tracing information.
5. requirements.txt - A file with the requirements and dependancies so that the script can be deployed in Lambda. For this project there weren't any external packages or dependancies required. 


## Architectural Choice Reasoning

I chose Python because it was a language I was fairly comfortable in and integrated fairly easily with AWS Lambda. Python also has some useful packages built in such as requests and regex. It is also great for tests.
 
I chose AWS Lambda due to its ability to run code without the need for provisioning or managing servers. From my research AWS Lambda, tends to scale requests easily which could be useful for future improvements and feature add ons for this project. Additionally, AWS Lambda provides the option of deploying code through zip files which is very convenient.

I chose API Gateway was selected as the front-end service to expose the Lambda functions as an API. I chose AWS gateways because it provides a very simple and effective way for creating and managing APIs and integrates with AWS Lambda very well. Also since in this project I was only using 3 functions, I didn't need a service that managed fully fledged applications like Elastic Beanstalk. I felt that this solution of using Lamda + Gateway was the best in terms of complexity and maintenance and it fulfills all the needs for this project. 

I used a REST API because it interacts well with standard HTTP requests which is necessary as the API is accessed by POST requests. Additionally, this project supports the assumption that all requests are stateless, since there is no relation between two contact tracing requests and hence no information has to be retained which is great for a REST API. Additionally, using REST APIs made it very easy for me to develop and test my code since there was a seperation between the server side and client side. 


## How to use the API

To call the functions, send a POST request to the API Gateway Invoke URL with a JSON payload containing the "function" and "params" keys. I have attached a file called 'testingAPI.py' which contains several different types of requests. I have also provided an example of an API call in python below. The function and param values must be passed as strings for the API to work.

### Example:
```python
import requests

api_url = "https://pae4znlv6b.execute-api.us-east-1.amazonaws.com/prod/testresource"  

# Call find_persons_by_location_and_date function
payload1 = {
    "function": "find_persons_by_location_and_date",
    "params": {
        "location": "Asshai",
        "date": "2021-02-01T00:00:00.000Z"
    }
}
response1 = requests.post(api_url, json=payload1)
print(response1.json())

```
Example Output
```python
    ['Bronn', 'Jon Snow', 'Sansa Stark']

```
## Error Handling

If an invalid function name is passed through the request the API will return an error. If an invalid/non existent date, location or name is given the API will simply return an empty list (a potential drawback). There is also some error handling if an invalid payload object is requested as well. 

## Cmd command to zip up files to upload to Lambda
Run this line in terminal to zip up the files so they can be deployed.

```cmd
tar -a -c -f app.zip requirements.txt app.py data.json
```
