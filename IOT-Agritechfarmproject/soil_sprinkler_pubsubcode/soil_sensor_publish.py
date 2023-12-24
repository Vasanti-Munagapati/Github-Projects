import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import random
import datetime
import sched
from Database import Database

# Define ENDPOINT, TOPIC, RELATOVE DIRECTORY for CERTIFICATE AND KEYS
ENDPOINT = "au5vba43plyvz-ats.iot.us-east-1.amazonaws.com"
PATH_TO_CERT = "..\\config"
TOPIC = "/devices/sensor_data"

# AWS class to create number of objects (devices)
class AWS():
    # Constructor that accepts client id that works as device id and file names for different devices
    # This method will obviosuly be called while creating the instance
    # It will create the MQTT client for AWS using the credentials
    # Connect operation will make sure that connection is established between the device and AWS MQTT
    def __init__(self, client, certificate, private_key):
        self.client_id = client
        self.device_id = client
        self.cert_path = certificate
        self.pvt_key_path = private_key
        self.root_path = "AmazonRootCA1.pem"
        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(self.client_id)
        self.myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(self.root_path, self.pvt_key_path, self.cert_path)

        # VM changes starts
        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        # VM changes ends
        self._connect()

    # Connect method to establish connection with AWS IoT core MQTT
    def _connect(self):
        self.myAWSIoTMQTTClient.connect()

    # This method will publish the data on MQTT 
    # Before publishing we are confiuguring message to be published on MQTT
    def publish(self,device_mapping):
        print('Begin Publish')
        for i in range (10):
            message = {}    
            value = float(random.normalvariate(99, 1.5))
            value = round(value, 1)

            # Get appropriate Sprinkler ID
            sprinkler_id =''
            for records in device_mapping['Items']:
                if self.device_id in records['mapped_to']:
                    sprinkler_id = records['sprinklerid']

            print('sprinkler id :',sprinkler_id)
            timestamp = str(datetime.datetime.now())
            message['deviceid'] = self.device_id
            message['dttimestamp'] = timestamp
            message['datatype'] = 'Temperature'
            message['value'] = value
            message['sprinkler_id'] = sprinkler_id
            messageJson = json.dumps(message)
            self.myAWSIoTMQTTClient.publish(TOPIC, messageJson, 1)
            print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
            time.sleep(0.1)

            # VM changes startes here
            message = {}
            value = float(random.normalvariate(90, 30.0))
            value = round(value, 1)
            timestamp = str(datetime.datetime.now())
            message['deviceid'] = self.device_id
            message['dttimestamp'] = timestamp
            message['datatype'] = 'Moisture'
            message['value'] = value
            message['sprinkler_id'] = sprinkler_id
            messageJson = json.dumps(message)
            self.myAWSIoTMQTTClient.publish(TOPIC, messageJson, 1)
            # VM changes ends here

            print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
            time.sleep(0.1)
        print('Publish End')

    # Disconect operation for each devices
    def disconnect(self):
        self.myAWSIoTMQTTClient.disconnect()