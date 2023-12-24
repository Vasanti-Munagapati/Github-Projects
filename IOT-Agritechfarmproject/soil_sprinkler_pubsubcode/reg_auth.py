'''
/********************************Point 2 of Project******************************************************************
 This file will have implementation related to the registration of devices and their mapping relationship and
 authorization logic

 Problem statement -
    Create a new table (agritech_device_data) using code.
    Create a new table (agritech_device_mapping_data) using code.

 Problem statement - point 2.b :
    1. config file will be used to register the data into database
    2. Mapping will also be populated using mapping table
 *********************************************************************************************************************/
 '''

import json
import datetime
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from Database import Database
import time
import numpy as np

class RegAuthModel:

    def __init__(self):
        self.database = Database()
        self.db_devicedata = self.database.db_createdevicedata()
        self.db_devicemapdata = self.database.db_createdevicemapdata()
        self._latest_error = ''

    def regdevandmappingdata(self):

        # Reading the configuration file
        f = open("config_devicedatareg.json")
        config = json.loads(f.read())
        f.close()

        # Initialising devices from the config.json file and assigning device_ids to each device
        device_config = []
        device_mapping = []
        for devices in config['devices']:
            for n in range(devices['device_count']):
                dev = {}
                dev_map={}
                dev['deviceid'] = devices['device_type'] + "_" + str(n)
                dev['device_type'] = devices['device_type']
                dev['description'] = devices['description']
                dev['device_status'] = devices['device_status']
                dev['lat'] = devices['device_lat']
                dev['lon'] = devices['device_lon']
                now = datetime.datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                dev['dttimestamp'] = dt_string

                item = json.loads(json.dumps(dev), parse_float=Decimal)
                response = self.db_devicedata.put_item(Item=item)
                time.sleep(1)

                if (dev['device_type'] == "soil_sensor"):
                    dev['topic'] = devices['publish_topic']
                    cnt_totalsoilsnsr = devices['device_count']
                elif(dev['device_type'] == "sprinkler_sensor"):
                    dev['topic'] = devices['subscribe_topic'] + str(devices['device_count']) + "/cmd"
                    cnt_totalspnksnsr = devices['device_count']
                    if n == 0:
                        index_slsnsr = 0
                    map_loop = int(cnt_totalsoilsnsr/cnt_totalspnksnsr)
                    dev_map['sprinklerid'] = dev['deviceid']
                    tmp_devmap = []
                    for i in range(index_slsnsr,index_slsnsr+map_loop):
                        tmp_devmap.append(device_config[i]['deviceid'])

                    dev_map['mapped_to'] = tmp_devmap
                    now = datetime.datetime.now()
                    dt_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                    dev_map['dttimestamp'] = dt_string
                    device_mapping.append(dev_map)

                    item = json.loads(json.dumps(dev_map), parse_float=Decimal)
                    response = self.db_devicemapdata.put_item(Item=item)
                    time.sleep(1)

                    index_slsnsr = index_slsnsr+map_loop

                device_config.append(dev)

        print(" Devices list : ",device_config)
        print("Device Mapping List :" ,device_mapping)
