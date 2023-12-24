
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25  

class Edge_Server:
    
    def __init__(self, instance_name):
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []
        self._devicesstatuslist = []
        self._errormessage =[]

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        # VM changes starts
        #print("Connected with result code " + str(result_code))
        client.subscribe("devices/registration")
        client.subscribe("devices/id/light/status/ack")
        client.subscribe("devices/id/ac/status/ack")
        client.subscribe("devices/type/light/status/ack")
        client.subscribe("devices/type/ac/status/ack")

        # control topic listed below
        client.subscribe("devices/id/light/setswtchstatus/ack")
        client.subscribe("devices/id/light/setintensitystatus/ack")
        client.subscribe("devices/id/ac/setswtchstatus/ack")
        client.subscribe("devices/id/ac/settemperaturestatus/ack")

        client.subscribe("devices/type/light/setdevicestatus/ack")
        client.subscribe("devices/type/ac/setdevicestatus/ack")

        client.subscribe("devices/id/light/INVLDintensity")
        client.subscribe("devices/id/light/temperature/err")
        client.subscribe("devices/id/ac/temperature/err")
        # VM changes ends
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        # VM changes starts
        self._devicesstatuslist=[]
        self._errormessage=[]
        message={}
        message = json.loads(msg.payload.decode('utf-8'))

        if (msg.topic == "devices/registration"):
            print("\nRegistration request is acknowledged for device " + message["device_id"] + " in " + message["room_type"])
            print("Request is processed for " + message["device_id"])

            self._registered_list.append(message)
            pub_message = {}
            publish_topic = "devices/registered/ack"
            pub_message["device_id"] = message["device_id"]
            self.client.publish(publish_topic,json.dumps(pub_message))
        elif ( (msg.topic == "devices/id/light/status/ack") or (msg.topic == "devices/id/ac/status/ack")):
            self._devicesstatuslist.append(message)
        elif ((msg.topic == "devices/type/light/status/ack") or (msg.topic == "devices/type/ac/status/ack")):
            self._devicesstatuslist.append(message)
        elif ((msg.topic == "devices/id/light/setswtchstatus/ack") or (msg.topic == "devices/id/ac/setswtchstatus/ack")):
            self._devicesstatuslist.append(message)
        elif ((msg.topic == "devices/id/light/setintensitystatus/ack") or (msg.topic == "devices/id/ac/settemperaturestatus/ack")):
            self._devicesstatuslist.append(message)
        elif ((msg.topic == "devices/type/light/setdevicestatus/ack") or (msg.topic == "devices/type/ac/setdevicestatus/ack")):
            self._devicesstatuslist.append(message)
        elif((msg.topic == "devices/id/light/INVLDintensity")):
            self._devicesstatuslist.append(message)
        elif((msg.topic == "devices/id/light/temperature/err")):
            self._errormessage.append(message)
        elif ((msg.topic == "devices/id/ac/temperature/err")):
            self._devicesstatuslist.append(message)
        # VM Action part is pending
        # VM changes ends

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_statusbydeviceid(self,id_device):
        self._devicesstatuslist = []
        publish_topic = "devices/id/" + id_device[:-2] + "/getstatus"
        pub_message = {}
        pub_message["device_id"] = id_device
        self.client.publish(publish_topic, json.dumps(pub_message))
        time.sleep(WAIT_TIME)
        print("Here is the current device-status for " + id_device + " : ", self._devicesstatuslist)
        return self._devicesstatuslist

    def get_statusbydevicetype(self,type_device):
        self._devicesstatuslist = []
        publish_topic = "devices/type/" + type_device + "/getstatus"
        pub_message = []
        self.client.publish(publish_topic, json.dumps(pub_message))
        time.sleep(WAIT_TIME)
        return self._devicesstatuslist

    def get_statusbyroomtype(self,type_room):
        self._devicesstatuslist = []
        deviceslist = []
        for x in self._registered_list:
            if type_room in x["room_type"]:
                deviceslist.append(x["device_id"])
        for device in deviceslist:
            publish_topic = "devices/id/" + device[:-2] + "/getstatus"
            pub_message = {}
            pub_message["device_id"] = device
            time.sleep(WAIT_TIME)
            self.client.publish(publish_topic, json.dumps(pub_message))
            time.sleep(WAIT_TIME)
            print("Here is the current device-status for " + device + " : " , self._devicesstatuslist)
        return self._devicesstatuslist

    def get_statusbyentirehome(self):
        self._devicesstatuslist = []
        deviceslist = []
        for x in self._registered_list:
            deviceslist.append(x["device_id"])
        for device in deviceslist:
            publish_topic = "devices/id/" + device[:-2] + "/getstatus"
            pub_message = {}
            pub_message["device_id"] = device
            time.sleep(WAIT_TIME)
            self.client.publish(publish_topic, json.dumps(pub_message))
            time.sleep(WAIT_TIME)
            print("Here is the current device-status for " + device + " : ", self._devicesstatuslist)
        return self._devicesstatuslist

    # Controlling and performing the operations on the devices
    # based on the request received
    def setbydeviceid(self,id_device,param,value):
        self._devicesstatuslist = []
        pub_message = {}
        pub_message["device_id"] = id_device
        if (param == 'switch_state'):
            publish_topic = "devices/id/" + id_device[:-2] + "/setswtchstatus"
            pub_message['switch_state'] = 'ON'
        elif (param == 'intensity'):
            publish_topic = "devices/id/" + id_device[:-2] + "/setintensitystatus"
            pub_message['intensity'] = value
        elif (param == 'temperature'):
            publish_topic = "devices/id/" + id_device[:-2] + "/settemperaturestatus"
            pub_message['temperature'] = value


        self.client.publish(publish_topic, json.dumps(pub_message))
        time.sleep(WAIT_TIME)
        print("Here is the current device-status for " + id_device + " : ", self._devicesstatuslist)
        return self._devicesstatuslist

    def setbydevicetype(self,type_device):
        self._devicesstatuslist = []
        pub_message = {}
        publish_topic = "devices/type/" + type_device + "/setdevicestatus"
        pub_message['switch_state'] = 'ON'
        if (type_device == 'light'):
            pub_message['intensity'] = "MEDIUM"
        elif (type_device == 'ac'):
            pub_message['temperature'] = 30

        self.client.publish(publish_topic, json.dumps(pub_message))
        time.sleep(WAIT_TIME)
        print("Here is the current device-status for " + type_device + " : ", self._devicesstatuslist)
        return self._devicesstatuslist

    def set_statusbyroomtype(self, type_room):
        self._devicesstatuslist = []
        deviceslist = []
        for x in self._registered_list:
            if type_room in x["room_type"]:
                deviceslist.append(x["device_id"])
        pub_message = {}
        for device in deviceslist:
            if (device[:-2] == 'light'):
                publish_topic = "devices/id/" + device[:-2] + "/setintensitystatus"
                pub_message['intensity'] = "MEDIUM"
            elif (device[:-2] == 'ac'):
                publish_topic = "devices/id/" + device[:-2]  + "/settemperaturestatus"
                pub_message['temperature'] = 31

            pub_message["device_id"] = device
            time.sleep(WAIT_TIME)
            self.client.publish(publish_topic, json.dumps(pub_message))
            time.sleep(WAIT_TIME)
            print("Here is the current device-status for " + device + " : ", self._devicesstatuslist)
        return self._devicesstatuslist

    def set_statusbyentirehome(self):
        self._devicesstatuslist = []
        deviceslist = []
        pub_message ={}
        for x in self._registered_list:
            deviceslist.append(x["device_id"])
        for device in deviceslist:
            publish_topic=""
            if (device[:-2] == 'light'):
                publish_topic = "devices/id/" + device[:-2] + "/setintensitystatus"
                if device == "light_5":
                    pub_message['intensity'] = "HIGH"
                else:
                    pub_message['intensity'] = "MEDIUM"
            elif (device[:-2] == 'ac'):
                publish_topic = "devices/id/" + device[:-2] + "/settemperaturestatus"
                pub_message['temperature'] = 30

            pub_message["device_id"] = device
            time.sleep(WAIT_TIME)
            self.client.publish(publish_topic, json.dumps(pub_message))
            time.sleep(WAIT_TIME)
            print("Here is the current device-status for " + device + " : ", self._devicesstatuslist)

            if((device == "light_2") or (device == "light_4")):
                self._errormessage =[]
                pub_msg = {}
                pub_topic = "devices/id/" + device[:-2] + "/settemperaturestatus"

                pub_msg["device_id"] = device
                pub_msg['temperature'] = 30
                self.client.publish(pub_topic, json.dumps(pub_msg))
                time.sleep(WAIT_TIME)
                print("Here is the current device-status for " + device + " : ", self._errormessage)
        return self._devicesstatuslist