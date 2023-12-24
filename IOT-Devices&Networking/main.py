import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25  

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)  

# Creating the light_device
print("******************* REGISTRATION OF THE DEVICES THROUGH SERVER *******************" )
print("\n******************* REGISTRATION OF LIGHT DEVICES INITIATED *******************")
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)  

light_device_2 = Light_Device("light_2", "Garage")
time.sleep(WAIT_TIME)

light_device_3 = Light_Device("light_3", "BR1")
time.sleep(WAIT_TIME)

light_device_4 = Light_Device("light_4", "BR2")
time.sleep(WAIT_TIME)

light_device_5 = Light_Device("light_5", "Living")
time.sleep(WAIT_TIME)

# Creating the ac_device
print("\n******************* REGISTRATION OF AC DEVICES INITIATED *******************")
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)

ac_device_2 = AC_Device("ac_2", "Living")
time.sleep(WAIT_TIME)

ac_device_3 = AC_Device("ac_3", "Living")
time.sleep(WAIT_TIME)

print("\n ******************* REGISTERED DEVICES ON THE SERVER *******************")
print("Fetching the list of registered devices from EdgeServer")
print("The Registered devices on Edge-Server:")
server_Rgtdlist = edge_server_1.get_registered_device_list()
id_deviceslst=[]
for x in server_Rgtdlist:
    id_deviceslst.append(x["device_id"])
print(id_deviceslst)

print("\n ******************* GETTING THE STATUS AND CONTROLLING THE DEVICES *******************")
print("\n******************* GETTING THE STATUS BY DEVICE_ID *******************")

device_statuslist={}
i=1
for device in id_deviceslst:
    if "light" in device:
        print("\nCommand ID " + str(i) + " is initiated")
        device_statuslist=edge_server_1.get_statusbydeviceid(device)
        time.sleep(WAIT_TIME)
        # print("Here is the current device-status for " + device + " : " + str(device_statuslist))
        print("Command ID " + str(i) + " is executed")
        i = i + 1
    elif "ac" in device:
        print("\nCommand ID " + str(i) + " is initiated")
        device_statuslist = edge_server_1.get_statusbydeviceid(device)
        time.sleep(WAIT_TIME)
        # print("Here is the current device-status for " + device + " : " + str(device_statuslist))
        print("Command ID " + str(i) + " is executed")
        i = i + 1

print("\n ******************* GETTING THE STATUS BY DEVICE_TYPE *******************")
print("\nStatus based on: LIGHT DEVICE TYPE ")
device_statuslist={}

print("Command ID " + str(i) + " is initiated")
device_statuslist = edge_server_1.get_statusbydevicetype("light")
print(device_statuslist)
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i =i +1

print("\nStatus based on: AC DEVICE TYPE ")
device_statuslist={}

print("Command ID " + str(i) + " is initiated")
device_statuslist = edge_server_1.get_statusbydevicetype("ac")
time.sleep(WAIT_TIME)
print(device_statuslist)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n ******************* GETTING THE STATUS BY ROOM_TYPE *******************")
print("\nStatus based on room: Living")
device_statuslist={}

print("Command ID " + str(i) + " is initiated")
device_statuslist = edge_server_1.get_statusbyroomtype("Living")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n ******************* GETTING THE STATUS BY ENTIRE_HOME *******************")

device_statuslist={}

print("Command ID " + str(i) + " is initiated")
device_statuslist = edge_server_1.get_statusbyentirehome()
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n ******************* SETTING UP THE STATUS AND CONTROLLING THE DEVICE_ID *******************")
print("\nControlling the devices based on ID : light_2")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydeviceid("light_2","switch_state","ON")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nControlling the devices based on ID : ac_2")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydeviceid("ac_2","switch_state","ON")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nControlling the devices based on ID : light_2")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydeviceid("light_2","intensity","HIGH")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nControlling the devices based on ID : ac_2")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydeviceid("ac_2","temperature",31)
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n ******************* SETTING UP THE STATUS AND CONTROLLING BY THE DEVICE_TYPE *******************")
print("\nControlling the devices based on TYPE : LIGHT")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydevicetype("light")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nControlling the devices based on TYPE : AC")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydevicetype("ac")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY ROOM *******************")
print("\nControlling the devices based on room: living")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.set_statusbyroomtype("Living")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n******************* SETTING UP THE STATUS AND CONTROLLING FOR INVALID REQUESTS *******************")
print("\nControlling the devices based on Entire room")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.set_statusbyentirehome()
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nControlling the devices based on ID : ac_2")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydeviceid("ac_2","temperature",36)
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nControlling the devices based on ID : light_1")
device_statuslist={}

print("Command ID " + str(i) + " is initiated")
device_statuslist = edge_server_1.setbydeviceid("light_1","intensity","DOUBLE")
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\n ******************* CURRENT STATUS BEFORE CLOSING THE PROGRAM *******************")
print("\nControlling the devices based on ID : light_1")
device_statuslist={}
print("Command ID " + str(i) + " is initiated")

device_statuslist = edge_server_1.setbydeviceid("light_1","intensity","MEDIUM")
time.sleep(WAIT_TIME)

device_statuslist = edge_server_1.setbydeviceid("light_2","intensity","MEDIUM")
time.sleep(WAIT_TIME)

device_statuslist = edge_server_1.setbydeviceid("light_3","intensity","MEDIUM")
time.sleep(WAIT_TIME)

device_statuslist = edge_server_1.setbydeviceid("light_4","intensity","MEDIUM")
time.sleep(WAIT_TIME)

device_statuslist = edge_server_1.setbydeviceid("light_5","intensity","HIGH")

device_statuslist = edge_server_1.setbydeviceid("ac_1","temperature",29)

device_statuslist = edge_server_1.setbydeviceid("ac_2","temperature",30)

device_statuslist = edge_server_1.setbydeviceid("ac_3","temperature",31)
time.sleep(WAIT_TIME)
print("Command ID " + str(i) + " is executed")
i=i+1

print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()
