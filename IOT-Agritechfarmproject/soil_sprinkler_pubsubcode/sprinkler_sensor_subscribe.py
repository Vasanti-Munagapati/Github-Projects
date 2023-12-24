import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import random
import datetime
import sched
import boto3
from Database import Database

# Define ENDPOINT, TOPIC, RELATOVE DIRECTORY for CERTIFICATE AND KEYS
ENDPOINT = "au5vba43plyvz-ats.iot.us-east-1.amazonaws.com"
PATH_TO_CERT = "..\\config"
TOPIC = "/devices/sprinkler"
certificate="sprinklercert.pem"
private_key="sprinklerprivate.key"

def customCallback(client, userdata, message):
    database = Database()

    device_data = database.db_getdevicedata()

    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    msg = json.loads(message.payload.decode('utf-8'))
    print(msg)
    print(device_data)
    if(msg['sprinkler_id'] == 'ALL'):
        for device_data['deviceid'] in 'sprinkler':
            dttimestamp = str(datetime.datetime.now())
            responsevalues = database.db_upddevicestatus(device_data['deviceid'],msg['set_status'],dttimestamp)
            time.sleep(0.1)
    else:
        dttimestamp = str(datetime.datetime.now())
        print(msg['sprinkler_id'])
        responsevalues = database.db_upddevicestatus(msg['sprinkler_id'],msg['set_status'],dttimestamp)
        time.sleep(0.1)

    print(responsevalues)

client_id = 'sprinkler_sensor'
cert_path = certificate
pvt_key_path = private_key
root_path = "AmazonRootCA1.pem"
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(root_path, pvt_key_path, cert_path)

myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()


# subscribe to the same topic in a loop forever
loopCount = 0
scheduler = sched.scheduler(time.time, time.sleep)

now = time.time()
while True:
    try :
            myAWSIoTMQTTClient.subscribe(TOPIC, 1,customCallback)
            time.sleep(2)
    except KeyboardInterrupt:
        break

print("Intiate the connection closing process from AWS.")
myAWSIoTMQTTClient.disconnect()
print("Connection closed.")
