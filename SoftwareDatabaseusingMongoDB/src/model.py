# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId

# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    # VM changes added accesslist
    def insert(self, username, email, role,accesslist=None):
        self._latest_error = ''

        user_document = self.find_by_username(username)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1

        # VM changes for Accesstype
        if (accesslist):
            useraxes_data = accesslist
            user_data = {'username': username, 'email': email, 'role': role,'user_device_access': useraxes_data}
        else:
            user_data = {'username': username, 'email': email, 'role': role}

        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)


# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        key = {'device_id': device_id}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if (device_document):
            self._latest_error = f'Device id {device_id} already exists'
            return -1
        
        device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        return self.find_by_object_id(device_obj_id)


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if (wdata_document):
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
        return self.find_by_object_id(wdata_obj_id)

# VM changes starts here for Point 2
class DailyReportModel:
    WEATHER_DATA_COLLECTION = 'weather_data'
    DAILY_REPORT_COLLECTION = 'daily_report'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
        self._db.drop_daily_report(DailyReportModel.DAILY_REPORT_COLLECTION) #VM Changes added to drop daily report for reexecution

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, collection, key):
        rdata_document = self._db.aggregate_data(collection, key)
        return rdata_document

    # Get multiple records from weather_data to create daily_reports
    def getaggregatedata(self,collection,pipeline1):
        return self.__find(collection,pipeline1)

    def createdailyreport(self):
        self._latest_error = ''

        # Get the Bulk data from weather_data
        pipeline1 = [
            {
                '$group': {'_id': {
                    'device_id': '$device_id',
                    'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}},
                },
                    'avg_value': {"$avg": "$value"},
                    'min_value': {"$min": "$value"},
                    'max_value': {'$max': '$value'}
                }
            }
        ]
        rdata_document = self.getaggregatedata(DailyReportModel.WEATHER_DATA_COLLECTION,pipeline1)

        #Start accumulation records in the required format in a dictionary
        dailyreport_data = []
        for doc in rdata_document:
            data = {
                'device_id': doc["_id"]["device_id"],
                'avg_value': round(doc["avg_value"],2),
                'min_value': round(doc["min_value"],2),
                'max_value': round(doc["max_value"],2),
                'date': doc["_id"]["date"]
            }
            dailyreport_data.append(data)

        # Insert multiple records in daily_report
        reportdataadded = self._db.insert_multiple_data(DailyReportModel.DAILY_REPORT_COLLECTION, dailyreport_data)
        return reportdataadded

    def displaydailyreport(self,device_id,from_date,to_date=None):
        if(to_date):
            pipeline1 = [
                {
                    '$match': {'device_id': device_id, 'date': {'$gte': from_date,'$lte': to_date}}
                }
            ]
        else:
            pipeline1 = [
                {
                    '$match': {'device_id': device_id, 'date': {'$eq': from_date}}
                }
            ]

        rdata_document = self.getaggregatedata(DailyReportModel.DAILY_REPORT_COLLECTION,pipeline1)
        for doc in rdata_document:
            print(doc)
        return True




# VM changes Ends here for Point 2
