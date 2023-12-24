from boto3.dynamodb.conditions import Key, Attr
import boto3
import json
import datetime
import base64
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb',region_name='us-east-1')

    table1 = dynamodb_res.Table('agritech_device_data')
    table2 = dynamodb_res.Table('weatherAPIdata')
    table3 = dynamodb_res.Table('agritech_device_alert')

    for payload in event['Records']:
        record = base64.b64decode(payload['kinesis']['data'])
        record = json.loads(record)

        device_id = record['deviceid']
        data_type = record['datatype']
        value = record['value']
        sprinkler_id = record['sprinkler_id']
        timestamp_val = record['dttimestamp']

        Keycondition = Key('deviceid').eq(sprinkler_id)
        deviceData = table1.query(KeyConditionExpression=Keycondition)

        sprinkler_status=deviceData['Items'][0]['device_status']
        lat = deviceData['Items'][0]['lat']
        lon = deviceData['Items'][0]['lon']

        Keycondition1 = (Key('lat').eq(lat) and Key('lon').eq(lon))
        weatherData = table2.get_item(Key={'lat':lat,'lon':lon})

        weather_status = weatherData['Item']['weather_status']

        dttimestamp = str(datetime.datetime.now())
        alert = False
        cmd={}
        if((weather_status =='Rain' or weather_status =='Drizzle') and sprinkler_status =='ON'):
            alert = True
            cmd['sprinkler_id'] = 'ALL'
            cmd['set_status'] = 'OFF'
            cmd['description'] = 'Weather is Rainy, Sending command to switch OFF ALL sprinkler sensors'
            cmd['timestamp'] = dttimestamp
        elif (data_type == 'Moisture'):
            if (value >70 and sprinkler_status =='ON'):
                alert = True
                cmd['sprinkler_id']=sprinkler_id
                cmd['set_status']= 'OFF'
                cmd['description'] = 'Moisture level is High, Sending command to switch OFF the sprinkler sensor'
                cmd['timestamp'] = dttimestamp
            elif(value <70 and sprinkler_status =='OFF'):
                alert = True
                cmd['sprinkler_id'] = sprinkler_id
                cmd['set_status'] = 'ON'
                cmd['description'] = 'Moisture level is Low, Sending command to switch ON the sprinkler sensor'
                cmd['timestamp'] = dttimestamp

        print("Alert",alert)
        print("command",cmd)
        if alert == True:
            iot_client = boto3.client('iot-data', region_name='us-east-1')
            response = iot_client.publish(topic="/devices/sprinkler", qos=1, payload=json.dumps(cmd))

            sns_client = boto3.client('sns', region_name='us-east-1')
            topic_arn = "arn:aws:sns:us-east-1:652627147462:agritech-alert-mail-sns-topic"

            sns_client.publish(TopicArn=topic_arn, Message=cmd['sprinkler_id'] + " " + cmd['description'])

            alert_rec = json.loads(json.dumps(cmd), parse_float=Decimal)
            table_response = table3.put_item(Item=alert_rec)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }









