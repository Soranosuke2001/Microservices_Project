# ACIT 3855 Microservices Project

Created By: Sora Schlegel
Last Updated: April 21st, 2024

This is a demonstration of how microservices work. It is a simple application where we receive data from a client and we process that data. The data is then shown on a webpage, Dashboard service.

## Service Descriptions

### Receiver Service

This service can receive 2 different types of events:

1. Item Transaction
2. Gun Statistic

Once the 2 events are received, these are processing and stored in a kafka topic. The Storage service will then process it later.

Note: Refer to the `Things we can do` section to view the JSON structure to send.

### Storage Service

There are a couple of things this service can do.

1. Storing the received data from the Receiver service to the MySQL database.

The Storage service will run a function in the background to check if there are new events received. If there are, it will process through each one and will update the database all at once when all of the new events in the kafka topic are processed.

2. Fetch data from the database with a specific time frame.

Not accessible to the public, but the Processing service will utilize these 2 GET endpoints. The 2 endpoints will return an array of events that are stored in the database from a specific time frame.

### Processing Service

This service will process all entries in the database periodically and update the SQLite database that stores the updated statistics.

The periodic function will fetch the new data from the last timestamp it fetched until the current time. It will then go through each event and update the SQLite database accordingly.

### Audit Service

This service will fetch a specific event from the kafka topic. It will return back the same object that was sent via the POST request to the Receiver service.

Note: This can be tested and available publicly. Refer to the `Things we can do` section for more details.

### Event Logger Service

This service will read a kafka topic, where each event recorded in the topic will correspond to a successful startup for either the Processing, Receiver, or Storage service. It will also record if there were more than 25 (by default) events that were processed at once by the Processing service. 

### Dashboard Service

This service is just a basic webpage where we can view some data.

1. Fetching Random Events

The service will periodically send requests to the Audit service to fetch a random event that was recorded and display it on the webpage.

2. Fetching Stats Data

The service will periodically send requests to the Processing service to fetch the latest entry in the SQLite database.

3. Fetching Event Logger Data

The service will periodically send requests to the Event Logger service to fetch the latest entry in the SQLite database.

4. Fetching Anomalies Detected

The service will periodically send requests to the Anomalies Detector service to fetch the latest entry in the SQLite database.

### Anomaly Detector Service

This service will read the kafka topic that was added by the Receiver service. It will then go through each entry and check for any anomalies within the data. In order to detect the anomalies, this must be set manually and integrated into the code. However, the threshold value can be configured using the `app_conf.yml` file. Any anomalies detected are saved to a stateful SQLite database.

Note: There is also a GET endpoint to view the list of anomalies detected, which is explained in the `Things we can do` section.

## Getting Started

1. On your machine, make sure you have Docker and Git installed
2. Clone this repository to your machine
   Note: You may have to change the configuration files.
   - In every folder, but `Dashboard` folder, there is a `config` folder. You may have to edit the `app_conf.yml` file with the correct configuration.
3. Go into the `deployment` directory and run the command:

```bash
docker compose up -d
```

This will pull images from my docker hub repo and run them in the background.

Note: we can check the status of each container using the following command:

```bash
docker ps
```

4. Once the containers are all running, you can follow along in the next section.

## Things we can do

### 1. Storing Data

We can send POST requests to the receiver service to store events. There are 2 endpoints that we can hit.

1. New Item Transaction (POST)

URL: `http://<ip-address>/receiver/new/item_transaction`

Body:

```json
{
  "transaction_id": "ed90a56d-fc89-4112-9dee-dd31fe9d55d9",
  "item_id": "8346cd90-aac9-4241-a644-1b2349ea505e",
  "user_id": "f33ce732-958d-4894-bacd-91512eecf3df",
  "transaction_date": "2024-02-05T12:31:10.001000+00:00",
  "item_price": 10
}
```

2. New Gun Stat (POST)

URL: `http://<ip-address>/receiver/new/gun_stat`

Body:

```json
{
  "gun_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "game_id": "1c3b5a4e-b4d3-42f9-afaa-b3618924bbe2",
  "user_id": "736bf87e-79e5-4d49-8e52-8e75d5e06f84",
  "num_missed_shots": 300,
  "num_body_shots": 800,
  "num_head_shots": 2121,
  "num_bullets_shot": 300
}
```

### 2. Using jMeter

Note: jMeter must be installed beforehand.

The `jmeter_test_plan.jmx` is currently configured to send 4000 POST requests to load test the receiver service.

Press the `Green Play button` to send the POST requests.

#### jMeter Configuration Adjustments

1. Under the `CSV Dataset Config`, you must change the directory to find the corresponding sample data. The dataset can be found in the `DataGenerator` folder of this repository. 

2. For both `HTTP Post Requests` change the IP address to the public IP address of the VM you have cloned this project to.

###3.  Fetching Data

Once some data is received, we can then fetch a specific event from the Audit service by specifying the `index` parameter. If the index value is not valid, then a 404 response will be returned.

Note: If you sent 10 POST requests, then you can fetch and event where the index value is 0 - 9. 

Gun Stat URL: `http://<ip-address>/audit_log/get/audit/gun_stats?index=<index>`

Item Transaction URL: `http://<ip-address>/audit_log/get/audit/purchase_transactions?index=<index>`

### 4. Viewing Data

Once there is data stored in the database, we can also view the data. The Dashboard service is a single web page application that will display some stats, calculated based on the stored data in the database, and some random data stored in the database.

URL: `http://<ip-address>`

### 5. Fetching Anomalies

There may have been invalid data sent to the server that is getting stored in the database. We can check the integrity of our data by performing a GET request to the endpoint. We can use Postman to perform the request or we can just visited the Dashboard service and view the results there as well.

If using Postman, the endpoint would be:

URL: `http://<ip-address>/anomalies`
