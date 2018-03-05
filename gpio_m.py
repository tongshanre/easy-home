import RPi.GPIO as GPIO
import socket

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
    def change_net(self,ip,port,gpio,status):
        s = socket.socket()
        s.connect(socket.getaddrinfo(ip,port)[0][-1])
        s.send(bytes(str(gpio)+'-'+str(status)))
        data = s.recv(100)
        s.close()
        return data
