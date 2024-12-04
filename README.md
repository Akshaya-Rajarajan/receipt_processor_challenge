## Receipt Processor Challenge - Home Test

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

## Extra Features and Assumptions:

- **RESTful API** for processing receipts and retrieving points.
- In-memory storage using dictionaries.
- Hashing of receipts to avoid uploading of redundant receipts and reduce time complexity in case of duplicate receipts.
- Assumed a proper receipt should have all the important keys like retailer, date, time, at least one item and total.
- Unit testing performed.
- Fully dockerized for easy deployment and testing.

## Installation and building the application
### Prerequisites:
1. Python 3.12 or latest release(3.13)
2. Visual Studio 
3. Docker Desktop

## How to build and run the application locally
To build the application and run it in your local server follow the below steps.

1. Clone my git repository as follows first in your command prompt/terminal 
```bash
git clone 
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

## How to use the Endpoints to process the receipts
1. After you start the server and hit the localhost:8000 link, you should get a 404 page not found page in which both the endpoints can be seen.
2. Now go to http://127.0.0.1:8000/receipts/process the post endpoint. 
3. Upload a receipt in JSON format and click the post button
4. It will return an id of the receipt as a JSON.
5. Now save the Id and hit the link http://localhost:8000/receipts/{id}/points.
6. This will return the points for that specific receipt in a JSON format.

## How to build the docker image locally and run the application from docker image
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
## How to run the application from docker image(prebuilt and pushed to dockerhub)
```bash 
docker run -p 8000:8000 <name of image>
```


