import json
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883


class Light_Device():

    # setting up the intensity choices for Smart Light Bulb  
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_state = "OFF"

    def _register_device(self, device_id, room_type, device_type):
       publish_topic = "devices/registration"

       # Initialize a dictionary to be sent as publish message
       pub_message = {}
       pub_message["device_id"] = device_id
       pub_message["device_type"] = "LIGHT"
       pub_message['room_type'] = room_type
       pub_message['switch_state'] = "OFF"
       pub_message['intensity'] = self._light_intensity
       self.client.publish(publish_topic,json.dumps(pub_message))


    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        #VM Changes starts
        #print("Connected with result code " + str(result_code))
        client.subscribe("devices/registered/ack")
        client.subscribe("devices/id/light/getstatus")
        client.subscribe("devices/type/light/getstatus")
        client.subscribe("devices/room_type/status")
        client.subscribe("devices/entire_home/status")

        # control topic listed below
        client.subscribe("devices/id/light/setswtchstatus")
        client.subscribe("devices/id/light/setintensitystatus")
        client.subscribe("devices/type/light/setdevicestatus")

        client.subscribe("devices/id/light/settemperaturestatus")
        #VM changes ends

    # Callback function - executed when the program gracefully disconnects from the broker
    def _on_disconnect(client, userdata, result_code):
        print("Disconnected with result code " + str(result_code))

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode('utf-8'))
        if (msg.topic == "devices/registered/ack"):
            if(message["device_id"] == self._device_id):
                self._device_registration_flag = True
                print("LIGHT-DEVICE Registered! - Registration status is available for "+ message["device_id"] + " : " + str(self._device_registration_flag))
        elif (msg.topic == ("devices/id/light/getstatus")):
            # Initialize a dictionary to be sent as publish message
            publish_topic = "devices/id/light/status/ack"
            pub_message = {}

            pub_message["device_id"] = message["device_id"]
            pub_message["device_type"] = "LIGHT"
            pub_message['switch_state'] = "OFF"
            pub_message['intensity'] = "LOW"
            self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/type/light/getstatus")):
            # Initialize a dictionary to be sent as publish message
            publish_topic = "devices/type/light/status/ack"
            temp_message ={}

            pub_msg = []
            temp_message["device_id"] = "light_1"
            temp_message["device_type"] = "LIGHT"
            temp_message['switch_state'] = "OFF"
            temp_message['intensity'] = "LOW"
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_2"
            temp_message["device_type"] = "LIGHT"
            temp_message['switch_state'] = "OFF"
            temp_message['intensity'] = "LOW"
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_3"
            temp_message["device_type"] = "LIGHT"
            temp_message['switch_state'] = "OFF"
            temp_message['intensity'] = "LOW"
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_4"
            temp_message["device_type"] = "LIGHT"
            temp_message['switch_state'] = "OFF"
            temp_message['intensity'] = "LOW"
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_5"
            temp_message["device_type"] = "LIGHT"
            temp_message['switch_state'] = "OFF"
            temp_message['intensity'] = "LOW"
            pub_msg.append(temp_message)

            self.client.publish(publish_topic, json.dumps(pub_msg))
        elif (msg.topic == ("devices/id/light/setswtchstatus")):
            self._device_id = message["device_id"]
            self._set_switch_status(message["switch_state"])

            publish_topic = "devices/id/light/setswtchstatus/ack"
            pub_message = {}

            pub_message = self._get_switch_status()
            self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/id/light/setintensitystatus")):
            self._device_id = message["device_id"]
            if (message['intensity'] not in ("LOW","MEDIUM","HIGH")):
                publish_topic = "devices/id/light/INVLDintensity"
                err_message = {}
                err_message["device_id"] = message["device_id"]
                err_message["error"] = "Intensity Change FAILED. Invalid Light Intensity level received"
                self.client.publish(publish_topic, json.dumps(err_message))
            else:
                self._set_light_intensity(message["intensity"])

                publish_topic = "devices/id/light/setintensitystatus/ack"
                pub_message = {}

                pub_message = self._get_light_intensity()
                self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/id/light/settemperaturestatus")):
            self._device_id = message["device_id"]

            publ_topic = "devices/id/light/temperature/err"
            err_message ={}
            err_message["error"] = "Temperature Change FAILED. Invalid temperature value received"
            self.client.publish(publ_topic, json.dumps(err_message))
        elif (msg.topic == ("devices/type/light/setdevicestatus")):
            publish_topic = "devices/type/light/setdevicestatus/ack"

            pub_msg = []
            temp_message ={}
            temp_message["device_id"] = "light_1"
            temp_message['switch_state'] = message['switch_state']
            temp_message['intensity'] = message['intensity']
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_2"
            temp_message['switch_state'] = message['switch_state']
            temp_message['intensity'] = message['intensity']
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_3"
            temp_message['switch_state'] = message['switch_state']
            temp_message['intensity'] = message['intensity']
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_4"
            temp_message['switch_state'] = message['switch_state']
            temp_message['intensity'] = message['intensity']
            pub_msg.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "light_5"
            temp_message['switch_state'] = message['switch_state']
            temp_message['intensity'] = message['intensity']
            pub_msg.append(temp_message)

            self.client.publish(publish_topic, json.dumps(pub_msg))

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        tmp_message ={}
        tmp_message["device_id"] = self._device_id
        tmp_message["switch_state"] = self._switch_state
        tmp_message["intensity"] = self._light_intensity
        return tmp_message

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_state = "ON"
        self._light_intensity = "LOW"

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        tmp_message = {}
        tmp_message["device_id"] = self._device_id
        tmp_message["switch_state"] = self._switch_state
        tmp_message["intensity"] = self._light_intensity
        return tmp_message

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        self._switch_state = "ON"
        self._light_intensity = light_intensity

