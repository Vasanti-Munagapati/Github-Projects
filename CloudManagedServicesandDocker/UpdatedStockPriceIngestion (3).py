import json
import boto3
import sys
import yfinance as yf
from decimal import Decimal
import time
import random
import datetime

# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc. 
# Further, you should call the static info api for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream

kinesis_client = boto3.client('kinesis', region_name = "us-east-1") #Modify this line of code according to your requirement.
from numpy import record

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(3)
stocks_list=["MSFT", "MVIS", "GOOG", "SPOT", "INO", "OCGN", "ABML", "RLLCF", "JNJ", "PSFE"]

# Example of pulling the data between 2 dates from yfinance API
total_record = []
for stock in stocks_list:
    print(stock)
    tmp_record=dict()
    data = yf.download(stock, start= yesterday, end= today, interval = '1h' )
    stock_value = yf.Ticker(stock).fast_info
    ## Add code to pull the data for the stocks specified in the doc
    for i in range(0,len(data)):
        tmp_record=dict()
        tmp_record["stock_id"] = stock
        tmp_closevalue = data.iloc[i]["Close"]
        tmp_record["close_value"]=round(tmp_closevalue,2)
        ## Add additional code to call 'info' API to get 52WeekHigh and 52WeekLow refering this this link - https://pypi.org/project/yfinance/
        tmp_record["yearhigh"]=round(stock_value["yearHigh"],2)
        tmp_record["yearlow"] = round(stock_value["yearLow"],2)
        tmp_record["timestamp"] = str(datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))

        print(tmp_record)
        # Add your code here to push data records to Kinesis stream.
        put_response = kinesis_client.put_record(
            StreamName="cldprjtkinesis_vm",
            Data=json.dumps(tmp_record),
            PartitionKey=stock)
        #total_record.append(tmp_record)

