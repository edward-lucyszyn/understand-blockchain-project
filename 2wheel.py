#create a class called 2_wheel_obj.py
class 2wheel:             #class name
    def __init__(self, serial_number):  #constructor
        self.serial_number = serial_number

    def get_has_serial_number(self):  #method
        # return the hash of the serial number
        return hashlib.sha256(self.serial_number.encode()).hexdigest()
