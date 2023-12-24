import boto3
import json
import datetime
import os
import base64

def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])

        payload_std = json.loads(payload)

        stock = payload_std['stock_id']
        close_value = int(payload_std['close_value'])
        yearhigh_val = int(payload_std['yearhigh'])
        yearlow_val = int(payload_std['yearlow'])
        timestamp_val = payload_std['timestamp']


        if (close_value >= ((yearhigh_val * 80) / 100) or close_value <= ((yearlow_val * 120) / 100)):
            table = dynamodb_res.Table('ystock_alert')
            result = table.put_item(Item={'stock_id': stock,'close_val': close_value,'yearhigh':yearhigh_val,'yearlow':yearlow_val,
                                          'alert_description':'close_value >= ((yearhigh_val * 80) / 100) or close_value <= ((yearlow_val * 120) / 100)',
                                          'timestamp':timestamp_val})

            client = boto3.client('sns', region_name='us-east-1')
            topic_arn = "arn:aws:sns:us-east-1:123156441955:cldprjtsnsystockalert_vm"

            try:
                client.publish(TopicArn=topic_arn, Message= " POI (point of interest) if it’s either >= 80% of 52WeekHigh or <= 120% of 52WeekLow", Subject="POI-detected")
                result = 1
            except Exception:
                result = 0

            print result
    return result