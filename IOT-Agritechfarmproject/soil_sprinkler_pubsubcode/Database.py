
'''
/*********************************************************************************************************************
    1.Create model and database classes to access DynamoDB.
    2.This is a class that will invoke and call the various databases and methods to fetch the data from the
    device_data and device_mapping_data table.
*********************************************************************************************************************/
 '''

import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time

class Database:

    def __init__(self):
        self._dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')

    def db_createdevicedata(self):
        db_devicedata = self._dynamodb_resource.create_table(
            TableName='agritech_device_data',
            KeySchema=[
                {
                    'AttributeName': 'deviceid',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'deviceid',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
        )
        time.sleep(5)
        print("Agri Tech Device Data Table status:", db_devicedata.table_status)
        return db_devicedata

    def db_createdevicemapdata(self):
        db_devicemapdata = self._dynamodb_resource.create_table(
                TableName='agritech_device_map_data',
                KeySchema=[
                    {
                        'AttributeName': 'sprinklerid',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'dttimestamp',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'sprinklerid',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'dttimestamp',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
        time.sleep(5)
        print("Agri Tech Device Mapping Data Table status:", db_devicemapdata.table_status)
        return db_devicemapdata

    def db_getdevicedata(self):
        self._db_devicedata_table = self._dynamodb_resource.Table('agritech_device_data')
        responsevalues = self._db_devicedata_table.scan()
        return responsevalues

    def db_upddevicestatus(self,device_id,device_status,device_timestamp):
        self._db_devicedata_table = self._dynamodb_resource.Table('agritech_device_data')

        responsevalues = self._db_devicedata_table.update_item(Key={ 'deviceid' : device_id },
                                                               UpdateExpression='SET device_status= :val1,dttimestamp= :val2',
                                                               ExpressionAttributeValues={ ':val1' : device_status,':val2': device_timestamp }
                                                               )
        return responsevalues

    def db_getdevicemappingdata(self):
        self._db_devicemapdata_table = self._dynamodb_resource.Table('agritech_device_map_data')
        responsevalues = self._db_devicemapdata_table.scan()
        return responsevalues

