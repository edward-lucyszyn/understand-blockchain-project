
import hashlib

class twowheel(object):             
    def __init__(self, serial_number, owner_sk):  
        self.serial_number = serial_number


    def get_has_serial_number(self):  #method
        # return the hash of the serial number
        return hashlib.sha256(self.serial_number.encode()).hexdigest()