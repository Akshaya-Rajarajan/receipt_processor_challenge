## Receipt Processor Challenge - Home Test
## Content

* [About the Application](#about-the-application)
* [Assumptions](#assumptions)
* [Extra Features](#extra-features)
* [Installation and Building the Application](#installation-and-building-the-application)
* [Commands to Build and Run the Application Locally](#commands-to-build-and-run-the-application-locally)
* [Commands to Build and Run the Docker Image Locally](#commands-to-build-and-run-the-docker-image-locally)
* [Commands to Pull and Run the Application From My Docker Image](#commands-to-pull-and-run-the-application-from-my-docker-image)
* [Testing the Application](#testing-the-application)
* [Project Structure](#project-structure)

## About the Application
This application is a web service built using **Python**, **Django Framework**, and **Rest API** to process receipts uploaded by the clients and reward them with points. 

Here, I have used two EndPoints:

1. `/receipts/process` (POST): this Api accepts the receipt as a JSON then processes the receipt and return the unique ID for the receipt as a JSON.
2. `/receipts/{id}/points` (GET): Retrieves the points for the receipt based on the ID passed. 

The points are calculated based on the rules mentioned below.

- One point for every alphanumeric character in the retailer name.
- 50 points if the total is a round dollar amount with no cents.
- 25 points if the total is a multiple of 0.25.
- 5 points for every two items on the receipt.
If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
- 6 points if the day in the purchase date is odd.
- 10 points if the time of purchase is after 2:00pm and before 4:00pm.

## Assumptions

- Assumed the JSON receipt should have all the important keys like retailer, date, time, at least one item and total.
- Assumed that the clients shouldn't be able to upload the same receipt twice.


## Extra Features
- Hashing of receipts to avoid uploading of redundant receipts and reduce time complexity in case of duplicate receipts.

<img src="images/Screenshot_duplicate_receipt.png" alt="Screenshot redundant receipt message" width="500">

- Raised exceptions using try and except to get expected input from the clients.
- Created unit test cases to check if each and every functionality work as expected.(check in receipts/views.py)
- RESTful API for processing receipts and retrieving points.
- In-memory storage using dictionaries.

## Installation and Building the Application
### Prerequisites:
1. Python 3.12 or latest release(3.13)
2. Visual Studio 
3. Docker Desktop

## Commands to Build and Run the Application Locally
To build the application and run it in your local server follow the below steps.

1. Clone my git repository as follows first in your command prompt/terminal 
```bash
git clone https://github.com/Akshaya-Rajarajan/receipt_processor_challenge.git
cd receipt_processor_challenge

```
2. open the code in your VS code tool and your application's terminal create a virtual environment and activate it.

```bash
python -m venv <give a name for your venv>
source <name of your venv>/bin/activate # for windows .\<name of your venv>\Scripts\activate
```
3. Install the dependencies in the requirements.txt file as given below.

```bash
pip install -r requirements.txt
```
4. Now you are all ready to run the application. Start the server with the following command.

```bash
python manage.py runserver
```
5. Once the server starts running you will get the api link. Press ctrl and click the link to open it in your browser. The api link should be like http://127.0.0.1:8000


## Commands to Build and Run the Docker Image Locally 
1. Build docker image as follows in your VS code application terminal.

```bash 
docker build -t <give a name for your image> .
```
2. Assign a tag to the image created.

```bash
docker tag <name of image> <your docker_name>/<name of image>
```
3. Push your image to docker.

```bash
docker push <your docker_name>/<name of image>
```
## Commands to Pull and Run the Application From My Docker Image
```bash 
docker pull akshayarajarajan/receipts-processor-akshaya
docker run -p 8000:8000 akshayarajarajan/receipts-processor-akshaya
```
## Testing the Application
You can use receipts like the one provided below to test the API using the HTTP client directly or using the API testing tools like Postman or Insomnia or you can check the test cases that I have written in receipts/test.py to do unit testing.

Steps to test the application using the HTTP client:

1. After you start the server and hit the localhost:8000 link, you should get a 404 page not found page in which both the endpoints can be seen.
2. Now go to http://localhost:8000/receipts/process the post endpoint. 
3. Upload a receipt in JSON format and click the post button

<img src="images/Screenshot_post.png" alt="Screenshot post request" width="500">

4. It will return an id of the receipt as a JSON.

<img src="images/Screenshot_post_response.png" alt="Screenshot post response" width="500">

5. Now save the Id and hit the link http://localhost:8000/receipts/{id}/points.
6. This will return the points for that specific receipt in a JSON format.

<img src="images/Screenshot_Get.png" alt="Screenshot get request" width="500">


#### How to run the test cases in the test.py 
In your application terminal run the below command:

```bash
python manage.py test
```
### Example of JSON Receipt:
```bash
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
```
## Project Structure

* ``` receipts/```: This the main app folder that contains the views.py, which contains the main logic and the API classes and the tests.py contains the unit test done for the logic.
* ```receipt_handler/urls.py```: This file contains all the url configurations of the applications.
* ``` manage.py ```: Django's command line utility
* ``` dockerfile ```: This file contains the configurations needed to build the docker image.
* ``` requirements.txt ```: This file contains the dependencies needed for this application.

