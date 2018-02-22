import RPi.GPIO as GPIO

class GPioUtil():
    __ports = [2,3,4,5]
    def __init__(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__ports, GPIO.OUT)
        except BaseException     as e :
            print e
    def change(self,id,status):
        id = int(id)
        if 2 <= id and 5 >= id :
            GPIO.output(id, status)
            return True;
        else:
            return False;
