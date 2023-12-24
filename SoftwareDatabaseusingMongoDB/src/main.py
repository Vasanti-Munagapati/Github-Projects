from model import UserModel, DeviceModel, WeatherDataModel,DailyReportModel
from datetime import datetime
from authmanager import AuthSuperUserService

# Vasanti code starts for 1.a
set_superuser = AuthSuperUserService()
superuser_name = 'admin'
superuser_document = set_superuser.setusrservice(superuser_name)

print(f'\nDoes {superuser_name} have admin access?')
useraccess = set_superuser.checkusraccess(superuser_document)
print(useraccess)

print(f'\nIs username based query possible for {superuser_name}?')
if (useraccess):
    # Vasanti code Ends for 1.a
    # Shows how to initiate and search in the users collection based on a username
    user_coll = UserModel()
    user_document = user_coll.find_by_username('admin')
    if (user_document):
        print(user_document)

    print(f'\nCan {superuser_name} add a new user?') # Vasanti code starts for 1.a
    # Shows a successful attempt on how to insert a user
    acctype=dict()
    acctype=[{'device_id': 'DT004', 'atype': 'r'}, {'device_id': 'DH003', 'atype': 'rw'}]
    user_document = user_coll.insert('user_3', 'test_3@example.com', 'default',acctype)
    if (user_document == -1):
        print(user_coll.latest_error)
    else:
        print(user_document)

    # Shows how to initiate and search in the devices collection based on a device id
    device_coll = DeviceModel()
    print(f'\nCan {superuser_name} access device DT002?') # VM code changes starts for point 1.b
    device_document = device_coll.find_by_device_id('DT002')
    if (device_document):
        print(device_document)

    # Shows a successful attempt on how to insert a new device
    print(f'\nCan {superuser_name} create device DT201?') # VM code changes starts for point 1.b
    device_document = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
    if (device_document == -1):
        print(device_coll.latest_error)
    else:
        print(device_document)

    # Shows how to initiate and search in the weather_data collection based on a device_id and timestamp
    wdata_coll = WeatherDataModel()
    print(f'\nCan {superuser_name} read DT002 device Weather data?') # VM code changes starts for point 1.b
    wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
    if (wdata_document):
        print(wdata_document)

    # Shows a failed attempt on how to insert a new data point
    print(f'\nCan {superuser_name} Create DT004 device Weather data?')  # VM code changes starts for point 1.b
    wdata_document = wdata_coll.insert('DT004', 12, datetime(2020, 12, 2, 13, 30, 0))
    if (wdata_document == -1):
        print(wdata_coll.latest_error)
    else:
        print(wdata_document)
    # VM starts pending code to add point daily_report point 2.a 2.b 2.c logic here
    print("\nGenerate daily reports ")
    report_coll = DailyReportModel()
    rdata_document = report_coll.createdailyreport()
    if (rdata_document == -1):
        print(report_coll.latest_error)

    print("Get daily report for one day")
    rdata_document = report_coll.displaydailyreport('DT004','2020-12-02')

    print("\nGet daily report for multiple days")
    rdata_document = report_coll.displaydailyreport('DT004', '2020-12-02','2020-12-04')

    # VM Ends pending code to add point daily_report point 2.a 2.b 2.c logic here

#*****************************Vasanti code starts for default user*********************************************
superuser_name = 'user_1'
superuser_document = set_superuser.setusrservice(superuser_name)

print(f'\nDoes {superuser_name} have admin access?')
useraccess = set_superuser.checkusraccess(superuser_document)
print(useraccess)

print(f'\nIs username based query possible for {superuser_name}?')
if (useraccess):
    # Vasanti code Ends for 1.a
    # Shows how to initiate and search in the users collection based on a username
    user_coll = UserModel()
    user_document = user_coll.find_by_username('admin')
    if (user_document):
        print(user_document)
else:
    print('Query' + set_superuser.latest_error)

print(f'\nCan {superuser_name} add a new user?') # Vasanti code starts for 1.a
if (useraccess):
    # Shows a successful attempt on how to insert a user
    user_document = user_coll.insert('test_3', 'test_3@example.com', 'default')
    if (user_document == -1):
        print(user_coll.latest_error)
    else:
        print(user_document)
else:
    print('Insert' + set_superuser.latest_error)

# Shows how to initiate and search in the devices collection based on a device id
device_coll = DeviceModel()
print(f'\nCan {superuser_name} access device DT004?') # VM code changes starts for point 1.b
chk_deviceaxes = set_superuser.checkdeviceaxeservice(superuser_document,'DT004','r')
if (chk_deviceaxes):
    device_document = device_coll.find_by_device_id('DT004')
    if (device_document):
        print(device_document)
else:
    print(set_superuser.latest_error)

print(f'\nCan {superuser_name} access device DT001?') # VM code changes starts for point 1.b
chk_deviceaxes = set_superuser.checkdeviceaxeservice(superuser_document,'DT001','r')
if (chk_deviceaxes):
    device_document = device_coll.find_by_device_id('DT001')
    if (device_document):
        print(device_document)
else:
    print(set_superuser.latest_error)

print(f'\nCan {superuser_name} create device DT202?') # VM code changes starts for point 1.b
chk_deviceaxes = set_superuser.checkdeviceaxeservice(superuser_document,'DT202','w')
if (chk_deviceaxes):
    # Shows a successful attempt on how to insert a new device
    device_document = device_coll.insert('DT202', 'Temperature Sensor', 'Temperature', 'Acme')
    if (device_document == -1):
        print(device_coll.latest_error)
    else:
        print(device_document)
else:
    print(set_superuser.latest_error)

# Shows how to initiate and search in the weather_data collection based on a device_id and timestamp
wdata_coll = WeatherDataModel()
print(f'\nCan {superuser_name} read DT001 device data?') # VM code changes starts for point 1.b
chk_deviceaxes = set_superuser.checkdeviceaxeservice(superuser_document,'DT001','r')
if (chk_deviceaxes):
    wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT001', datetime(2020, 12, 2, 13, 30, 0))
    if (wdata_document):
        print(wdata_document)
else:
        print(set_superuser.latest_error)

# Shows a failed attempt on how to insert a new data point
print(f'\nCan {superuser_name} Create DT002 device data?')  # VM code changes starts for point 1.b
chk_deviceaxes = set_superuser.checkdeviceaxeservice(superuser_document,'DT002','w')
if (chk_deviceaxes):
    wdata_document = wdata_coll.insert('DT002', 12, datetime(2020, 12, 2, 13, 30, 0))
    if (wdata_document == -1):
        print(wdata_coll.latest_error)
    else:
        print(wdata_document)
else:
        print(set_superuser.latest_error)
# VM code changes for 1.a and 1.b ends here