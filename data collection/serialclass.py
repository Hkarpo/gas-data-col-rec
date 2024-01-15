import serial
from makeandwrite import *
from getdata import *
class Serialclass():
    global baudrate
    baudrate = 9600
    #定的一致
    def __init__(self,sname,title):
        self.sname=sname
        self.title=title
        self.ser=serial.Serial(self.sname,baudrate)
        makedir(title)
    def get_raw_data(self):
        data=self.ser.readline().decode('utf-8')
        return data
    def flush_load(self):
        self.ser.flush()
    def openbeng(self):
        self.ser.write("0".encode())
    def singledata(self):
        print(self.readline())
    def closebeng(self):
        self.ser.write("1".encode())

def ser_flush(S):
    S.flush_load()

def ser_flush_all(slist):
    for i in slist:
        i.flush_load()
    # ser.flush_load()