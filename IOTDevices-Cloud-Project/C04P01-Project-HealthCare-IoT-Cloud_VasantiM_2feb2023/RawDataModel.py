'''
/********************************Point 1 of Project******************************************************************
    This file will process the raw data that was created and pushed in the bsm_raw_data table by BedSideMonitor.py.
    1.This file will get sensor wise data for each device and create csv file against device + datype which then will
        be used by aggregate model to apply aggregate functionality
*********************************************************************************************************************/
 '''

import csv
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from Database import Database
import datetime

class RawDataModel:

    def __init__(self):
        self.database = Database()
        self._latest_error = ''

    def get_bsmrawdata(self,device_id):
        device_ids = device_id

        list_filename=[]
        for device_id in device_ids:
            device_types=["Temperature","SPO2","HeartRate"]
            for dtype in device_types:
                responsevalues = self.database.db_getbsmrawdata(device_id,dtype)
                if len(responsevalues['Items']) != 0:
                    items = responsevalues['Items']
                    columns = items[0].keys()
                    filename = device_id + '-' + dtype + '-' + '2023-02-02'+".csv"
                    list_filename.append({'deviceid':device_id,'datatype':dtype,'filename':filename})
                    print(filename)
                    with open(filename, 'w') as f:
                        dict_writer = csv.DictWriter(f, columns)
                        dict_writer.writeheader()
                        for i in items:
                            dict_writer.writerow(i)

        return list_filename
