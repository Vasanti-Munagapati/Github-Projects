
import json
import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        publish_topic = "devices/registration"
        {'device_id': 'ac_2', 'switch_state': 'OFF', 'temperature': 22}
        # Initialize a dictionary to be sent as publish message
        pub_message = {}
        pub_message["device_id"] = device_id
        pub_message["device_type"] = "AC"
        pub_message['room_type'] = room_type
        pub_message['switch_state'] = "OFF"
        pub_message['temperature'] = 22
        self.client.publish(publish_topic, json.dumps(pub_message))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        # VM Changes starts
        # print("Connected with result code " + str(result_code))
        client.subscribe("devices/registered/ack")
        client.subscribe("devices/id/ac/getstatus")
        client.subscribe("devices/type/ac/getstatus")
        client.subscribe("devices/room_type/status")
        client.subscribe("devices/entire_home/status")

        # control topic listed below
        client.subscribe("devices/id/ac/setswtchstatus")
        client.subscribe("devices/id/ac/settemperaturestatus")
        client.subscribe("devices/type/ac/setdevicestatus")
        # VM changes ends

    # Callback function - executed when the program gracefully disconnects from the broker
    def _on_disconnect(client, userdata, result_code):
        print("Disconnected with result code " + str(result_code))

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode('utf-8'))
        if (msg.topic == "devices/registered/ack"):
            if (message["device_id"] == self._device_id):
                self._device_registration_flag = True
                print("AC-DEVICE Registered! - Registration status is available for " + message["device_id"] + " : " + str(self._device_registration_flag))
        elif (msg.topic == ("devices/id/ac/getstatus")):
            # Initialize a dictionary to be sent as publish message
            publish_topic = "devices/id/ac/status/ack"
            pub_message = {}

            pub_message["device_id"] = message["device_id"]
            pub_message["device_type"] = "AC"
            pub_message['switch_state'] = "OFF"
            pub_message['temperature'] = 22
            self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/type/ac/getstatus")):
            # Initialize a dictionary to be sent as publish message
            publish_topic = "devices/type/ac/status/ack"
            pub_message=[]

            temp_message = {}
            temp_message["device_id"] = "ac_1"
            temp_message["device_type"] = "AC"
            temp_message['switch_state'] = "OFF"
            temp_message['temperature'] = 22
            pub_message.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "ac_2"
            temp_message["device_type"] = "AC"
            temp_message['switch_state'] = "OFF"
            temp_message['temperature'] = 22
            pub_message.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "ac_3"
            temp_message["device_type"] = "AC"
            temp_message['switch_state'] = "OFF"
            temp_message['temperature'] = 22
            pub_message.append(temp_message)

            self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/id/ac/setswtchstatus")):
            self._device_id = message["device_id"]
            self._set_switch_status(message["switch_state"])

            publish_topic = "devices/id/ac/setswtchstatus/ack"
            pub_message = {}

            pub_message = self._get_switch_status()
            self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/id/ac/settemperaturestatus")):
            self._device_id = message["device_id"]
            temp_value = message["temperature"]
            if ((temp_value < 18) or (temp_value > 32)):
                publish_topic = "devices/id/ac/temperature/err"
                err_message = {}
                err_message["device_id"] = message["device_id"]
                err_message["error"] = "Temperature Change FAILED. Invalid temperature value received"
                self.client.publish(publish_topic, json.dumps(err_message))
            else:
                self._set_temperature(message["temperature"])
                publish_topic = "devices/id/ac/settemperaturestatus/ack"
                pub_message = {}

                pub_message = self._get_temperature()
                self.client.publish(publish_topic, json.dumps(pub_message))
        elif (msg.topic == ("devices/type/ac/setdevicestatus")):
            # Initialize a dictionary to be sent as publish message
            publish_topic = "devices/type/ac/setdevicestatus/ack"
            pub_message=[]

            temp_message = {}
            temp_message["device_id"] = "ac_1"
            temp_message['switch_state'] = message['switch_state']
            temp_message['temperature'] = message['temperature']
            pub_message.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "ac_2"
            temp_message['switch_state'] = message['switch_state']
            temp_message['temperature'] = message['temperature']
            pub_message.append(temp_message)

            temp_message = {}
            temp_message["device_id"] = "ac_3"
            temp_message['switch_state'] = message['switch_state']
            temp_message['temperature'] = message['temperature']
            pub_message.append(temp_message)

            self.client.publish(publish_topic, json.dumps(pub_message))

    # Getting the current switch status of devices
    def _get_switch_status(self):
        tmp_message = {}
        tmp_message["device_id"] = self._device_id
        tmp_message["switch_state"] = self._switch_state
        tmp_message["temperature"] = self._temperature
        return tmp_message

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_state = "ON"
        self._temperature = 22

    # Getting the temperature for the devices
    def _get_temperature(self):
        tmp_message = {}
        tmp_message["device_id"] = self._device_id
        tmp_message["switch_state"] = self._switch_state
        tmp_message["temperature"] = self._temperature
        return tmp_message

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        self._switch_state = "ON"
        self._temperature = temperature
    
