from autoprovision import *
from reg_auth import *
from soil_sensor_publish import *
from Database import Database
import pandas as pd
from IPython.display import display

###### Auto Provisioning IOT things ,policies,downloading certificates and keys ##########
createThing()

##### Register Devices and their mapping in aws dynamodb#######################
Regis_devi = RegAuthModel()
Regis_devi.regdevandmappingdata()

# Get registered Device Configuration
database = Database()

device_config = []
device_config = database.db_getdevicedata()
print("Registered Devices list :", device_config)
print(type(device_config))

# Get Device Mapping
device_mapping = []
device_mapping = database.db_getdevicemappingdata()
print("Mapped devices list :", device_mapping)

##### Call soil sensor publisher to publish data###############################

devices_list = ['soil_sensor_1', 'soil_sensor_2','soil_sensor_3','soil_sensor_4','soil_sensor_11','soil_sensor_12','soil_sensor_13','soil_sensor_7', 'soil_sensor_15', 'soil_sensor_22']
auth_devices = []
# Authorization logic
for records in device_config['Items']:
    if records['deviceid'] in devices_list:
        auth_devices.append(records['deviceid'])

print(auth_devices)
i = 1
for soil_sensor in auth_devices:
    # SOil sensor device Objects
    soil = AWS(soil_sensor, "soilsensorcert.pem", "soilsensorprivate.key")
    soil.publish(device_mapping)

    dttimestamp = str(datetime.datetime.now())

    response = database.db_upddevicestatus(soil_sensor, 'ON', dttimestamp)
    print(response)


######### Display status of different sensors##############################
time.sleep(30)
for i in range(5):
    device_details = database.db_getdevicedata()
    df = pd.DataFrame(device_details['Items'])
    df1 = df[['deviceid','device_status','dttimestamp']]
    print(df1)
    time.sleep(10)