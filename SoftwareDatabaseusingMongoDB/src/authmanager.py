# Imports Database class from the project to provide basic functionality for database access
from database import Database

# Vasanti code starts for setting the username and role check problem 1.a
class AuthSuperUserService:
    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    def setusrservice(self,username):
        #this code will return the super user collection details to the cient
        key = {'username': username}
        user_document = self._db.get_single_data('users', key)
        return user_document

    def checkusraccess(self,usercollection):
        #this function should determine whether access is default or admin
        #if default should return error so that
        if (usercollection):
            if (usercollection.get('role') != "admin"):
                self._latest_error = ' failed, Admin access required!'
                return False
        return True

    def checkdeviceaxeservice(self,usercollection,device_id,operation):
        usr_devicesaccess = usercollection['user_device_access']
        accesstype ="x"

        # Get access type for the respective device
        for devicedoc in usr_devicesaccess:
            if (device_id in devicedoc['device_id']):
                accesstype = devicedoc['atype']
                break

        if (operation == 'r'):
            if(accesstype == 'r' or accesstype == 'rw'):
                return 1
            else:
                self._latest_error = f'Read access not allowed to {device_id}'
        elif (operation == 'w' ):
            if(accesstype == 'rw'):
                return 1
            else:
                self._latest_error = f'Write access not allowed to {device_id}'
                return 0
        else:
            self._latest_error = f'Read access not allowed to {device_id}'
            return 0


    def checksuweatheraxeservice(self,usercollection,device_id,operation):
        pass


# Vasanti code Ends for setting the username and role check problem 1.a