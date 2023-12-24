import requests
import json
import pprint
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal


def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    api_key = "0f8b321c68552dff33eeb5625f971c39"
    lat = 19.0760
    lon = 72.8777

    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lon": lon,
        'lat': lat,
        "units": "metric",
        "appid": api_key
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    record = {}
    record['city'] = data['name']
    record['lat'] = lat
    record['lon'] = lon
    record['temperature'] = data["main"]["temp"]
    record['humidity'] = data["main"]["humidity"]
    record['weather_status'] = data["weather"][0]["main"]
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    record['dttimestamp'] = dt_string

    print("Record : ", record)
    print(data)

    weather_rec = json.loads(json.dumps(record), parse_float=Decimal)
    table = dynamodb_res.Table('weatherAPIdata')

    rec_exist = table.get_item(Key={'lat': weather_rec['lat'], 'lon': weather_rec['lon']})

    if 'Items' in rec_exist:
        response = table.update_item(
            Key={'lat': weather_rec['lat'], 'lon': weather_rec['lon']},
            UpdateExpression='set city = :city , temperature = :temprtr, humidity = :hum , weather_status = :status, dttimestamp = :tstmp',
            ExpressionAttributeValues={
                ':city': record['city'],
                ':temprtr': weather_rec['temperature'],
                ':hum': weather_rec['humidity'],
                ':status': weather_rec['weather_status'],
                ':tstmp': weather_rec['dttimestamp']

            }
        )
    else:
        response = table.put_item(Item=weather_rec)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }