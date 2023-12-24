'''
/********************************************************************************************************************
    This will be the driver code that should be invoked to perform the aggregation operation and alert operation on
    the inserted data that is available in the raw form in one of the tables.
*********************************************************************************************************************/
 '''

from RawDataModel import RawDataModel
from AggregateModel import AggregateModel
from AlertDataModel import AlertDataModel

super_bsmrawdata = RawDataModel()
super_deviceid = ["BSM_G101","BSM_G102"]
lst_filename = super_bsmrawdata.get_bsmrawdata(super_deviceid)


super_bsmaggdata = AggregateModel()

for i in lst_filename:
    print("\n Aggregating data for device :",i['deviceid'])
    super_bsmaggdata.aggregatefunc(i['deviceid'],i['datatype'],i['filename'])

super_alertdatamodel = AlertDataModel()
super_alertdatamodel.find_and_raise_alert("2023-02-02 13:04:00","2023-02-02 13:52:00")
