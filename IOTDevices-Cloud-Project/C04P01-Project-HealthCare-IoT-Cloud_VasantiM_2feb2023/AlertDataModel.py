'''
/********************************Point 3 of Project******************************************************************
 Problem statement - point 3.a :
    This is a file that will access the created rules and will detect the anomaly values based on the parsed rule.
 Problem statement - point 3.b :
    The detected output will then be pushed in the bsm_alerts
 ********************************************************************************************************************/
 '''
import boto3
import time
import json
import datetime
from Database import Database
from decimal import Decimal

class AlertDataModel:

    def __init__(self):
        self.database = Database()
        self.bsmalertstable = self.database.db_createbsmalerts()
        self._latest_error = ''

    def readrulesconfiguration(self):
        # Reading the configuration file
        f = open("Rule.json")
        rule_config = json.loads(f.read())
        f.close()

        # Initialising devices from the Rule.json file and assigning device_ids to each device
        dev_ruleconfig = []
        for devices in rule_config['devices']:
            dev = {}
            dev['deviceid'] = devices['deviceid']
            dev['datatype'] = devices['datatype']
            dev['avg_min'] = devices['avg_min']
            dev['avg_max'] = devices['avg_max']
            dev['trigger_count'] = devices['trigger_count']
            dev_ruleconfig.append(dev)
        return dev_ruleconfig

    def find_and_raise_alert(self,for_starttime,for_endtime):
        device_ruleconfig = self.readrulesconfiguration()

        with self.bsmalertstable.batch_writer() as batch:
            for device_rule in device_ruleconfig:
                print("\n Processing rules for device :",device_rule['deviceid'])
                responsevalues = self.database.db_getbsmaggdata(device_rule['deviceid'],device_rule['datatype'],for_starttime,for_endtime)
                seq_recordcnt = 0

                if len(responsevalues['Items']) != 0:
                    lst_bsmalertsdata=[]
                    for item in responsevalues['Items']:
                        temp_ruledescription=""
                        tmp_bsmalertsdata={}
                        readings = item

                        if (int(readings['avg_value']) < device_rule['avg_min']) or (int(readings['avg_value']) > device_rule['avg_max']):
                            seq_recordcnt = seq_recordcnt + 1
                            tmp_bsmalertsdata['deviceid'] = device_rule['deviceid']
                            tmp_bsmalertsdata['datatype'] = device_rule['datatype']
                            tmp_bsmalertsdata['avg_value'] = readings['avg_value']
                            tmp_bsmalertsdata['from_rawtimestamp'] = readings['from_rawtimestamp']
                            temp_ruledescription = str(
                                device_rule['trigger_count']) + " continuous aggregated (at the minute level) " \
                                                   + str(readings['avg_value']) + " are outside the " + str(
                                device_rule['avg_min']) \
                                                   + "/" + str(device_rule['avg_max'])
                            tmp_bsmalertsdata['rule'] = {'description': temp_ruledescription}
                            now = datetime.datetime.now()
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                            tmp_bsmalertsdata['timestamp'] = dt_string
                            lst_bsmalertsdata.append(tmp_bsmalertsdata)

                            if (seq_recordcnt == device_rule['trigger_count']):
                                for records in lst_bsmalertsdata:
                                    print("Alert for device_id " + records['deviceid'] + " for sensor type " +  records['deviceid'] + " starting at " + records['from_rawtimestamp'])
                                    print(" for rule : ",temp_ruledescription)
                                    time.sleep(1)
                                    response = batch.put_item(Item=records)
                                    time.sleep(1)

                                seq_recordcnt = 0
                                lst_bsmalertsdata=[]
                        else:
                            seq_recordcnt = 0
                            lst_bsmalertsdata=[]


