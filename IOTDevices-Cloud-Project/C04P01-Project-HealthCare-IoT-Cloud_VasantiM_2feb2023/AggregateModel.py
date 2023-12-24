'''
/********************************Point 2 of Project******************************************************************
 This file will have implementation related to the aggregation on the raw data

 Problem statement - point 2.a :
    Create a new table (bsm_agg_data) using code.

 Problem statement - point 2.b :
    1. File created at device id and sensor level by raw data model would be used
    2. Records from the file would be extracted at the minute level
    3. upon those extracted records minimum ,maximum and average values would be found by using panda library
    4. these values then will be stored in bsm_agg_data along with columns
        a.device id
        b.datatype
        c.min_val
        d.max_val
        e.avg_val
        f.from_rawdatatime
        g.to_rawdatatime
        h.timestamp

 *********************************************************************************************************************/
 '''

import json
import datetime
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from Database import Database
import pandas as pd
import time

class AggregateModel:

    def __init__(self):
        self.database = Database()
        self.bsmaggregatetable = self.database.db_createbsmaggdata()
        self._latest_error = ''

    def aggregatefunc(self,device_id,datatype,sensor_filename):
        print(sensor_filename)
        df_temp = pd.read_csv(sensor_filename)
        start_date = pd.to_datetime(df_temp['timestamp'].min())
        file_enddate = pd.to_datetime(df_temp['timestamp'].max())

        tmp_enddate = file_enddate.strftime('%Y-%m-%d %H:%M:00') #converting second value to zero
        end_date = datetime.datetime.strptime(tmp_enddate,'%Y-%m-%d %H:%M:00')

        total_count = 0

        tmp_current_time = start_date.strftime('%Y-%m-%d %H:%M:00') #converting second value to zero
        current_time=datetime.datetime.strptime(tmp_current_time,'%Y-%m-%d %H:%M:00')

        list_bsmaggrdata=[]
        with self.bsmaggregatetable.batch_writer() as batch:
            while(str(current_time) <= str(end_date)):
                tmp_bsmaggrdata = {}
                Next_timeframe=current_time + datetime.timedelta(seconds=60)

                after_start_date = df_temp["timestamp"] >= str(current_time)
                before_end_date = df_temp["timestamp"] <= str(Next_timeframe)
                between_two_dates = after_start_date & before_end_date

                df2 = df_temp.loc[between_two_dates]
                if(len(df2) !=0):
                    min1 = float(df2['value'].min())
                    max1 = float(df2['value'].max())
                    sum1 = float(df2['value'].sum())
                    count1 = df2['value'].count()
                    avg1 = round(sum1/count1,1)

                    tmp_bsmaggrdata['deviceid']=device_id
                    tmp_bsmaggrdata['datatype'] = datatype
                    tmp_bsmaggrdata['min_value'] = round(min1,1)
                    tmp_bsmaggrdata['max_value'] = round(max1,1)
                    tmp_bsmaggrdata['avg_value'] = avg1
                    tmp_bsmaggrdata['from_rawtimestamp'] = str(current_time)
                    tmp_bsmaggrdata['to_rawtimestamp'] = str(Next_timeframe)
                    now = datetime.datetime.now()
                    dt_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                    tmp_bsmaggrdata['timestamp'] = dt_string

                    time.sleep(1)
                    item = json.loads(json.dumps(tmp_bsmaggrdata), parse_float=Decimal)

                    time.sleep(1)
                    response = batch.put_item(Item=item)
                    time.sleep(1)

                total_count=total_count + 1
                current_time = Next_timeframe



