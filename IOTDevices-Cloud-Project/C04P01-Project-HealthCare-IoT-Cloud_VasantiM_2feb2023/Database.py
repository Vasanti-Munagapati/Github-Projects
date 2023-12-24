
'''
/*********************************************************************************************************************
    1.Create model and database classes to access DynamoDB.
    2.This is a class that will invoke and call the various databases and methods to fetch and store the data in the
    bsm_agg_data table.
*********************************************************************************************************************/
 '''



import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time

class Database:

    def __init__(self):
        self._dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')

    def db_getbsmrawdata(self, device_id, dtype):
        self._db_bsmraw_table = self._dynamodb_resource.Table('bsm_raw_data')
        Keycondition = Key('deviceid').eq(device_id)
        Filtercondition = Key('datatype').eq(dtype)
        responsevalues = self._db_bsmraw_table.query(KeyConditionExpression=Keycondition, FilterExpression=Filtercondition)
        return responsevalues

    def db_createbsmaggdata(self):
        # db_bsmaggregatetable = self._dynamodb_resource.Table('bsm_agg_data')
        db_bsmaggregatetable = self._dynamodb_resource.create_table(
            TableName='bsm_agg_data',
            KeySchema=[
                {
                    'AttributeName': 'deviceid',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'deviceid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
        )
        time.sleep(5)
        print("bsm aggregate Table status:", db_bsmaggregatetable.table_status)

        return db_bsmaggregatetable

    def db_createbsmalerts(self):
        # db_bsmaggregatetable = self._dynamodb_resource.Table('bsm_agg_data')
        db_bsmalertstable = self._dynamodb_resource.create_table(
            TableName='bsm_alerts',
            KeySchema=[
                {
                    'AttributeName': 'deviceid',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'deviceid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
        )
        time.sleep(5)
        print("bsm alerts Table status:", db_bsmalertstable.table_status)
        return db_bsmalertstable

    def db_getbsmaggdata(self, device_id, dtype,start_time,end_time):
        self._db_bsmaggtable = self._dynamodb_resource.Table('bsm_agg_data')
        Keycondition = Key('deviceid').eq(device_id)
        Filtercondition = Key('datatype').eq(dtype) & Key('from_rawtimestamp').between(start_time, end_time)
        responsevalues = self._db_bsmaggtable.query(KeyConditionExpression=Keycondition, FilterExpression=Filtercondition)
        return responsevalues


    def db_deletetable(self,db_bsmaggregatetable):
        db_bsmaggregatetable.delete()