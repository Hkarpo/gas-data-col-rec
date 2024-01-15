# This is a sample Python script.
import random
import time
import serial
import csv
import os
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# 构建串口类
class Serialclass():
    global baudrate
    baudrate = 9600
    #定的一致
    def __init__(self,sname,title,label):
        self.sname=sname
        self.title=title
        self.ser=serial.Serial(self.sname,baudrate)
        self.label=label
        #电子鼻编码内参
        makedir(title)
    def get_raw_data(self):
        data=self.ser.readline().decode('utf-8')
        return data
    def flush_load(self):
        self.ser.flush()


def single_sen(S,dataload):
    d = time.localtime()
    cur_time1 = time.strftime('%m.%d.%H%M%S', d)
    try:
        value = S.get_raw_data()
        dataArray = value.split(',')
        # print(dataArray)
    except(ValueError, PermissionError):
        ser_flush_all(S)
        dataArray = []
        print("串口问题报错", cur_time1)
        for c in range(23):
            dataArray.append('nan')
    dataload.append([cur_time1] + dataArray)

#清空串口
def ser_flush(S):
    S.flush_load()

#多电子鼻清空
def ser_flush_all(slist):
    for i in slist:
        i.flush_load()

#时间记录
def timecount(d,h,m,s):
    time=s+60*m+60*60*h+60*60*24*d
    return time

#判断是否可以重启
def getreboot(start,end,out,blow):
    if end-start-out-blow >0:
        return '1'
    else:
        return '0'

#判断是否可以输出结果
def getoutput(start,end,out,classnum):
    if end-start>out:
        return str(classnum)
    else:
        return '0'
def refresh_status(a,b,f):
    with open(f, "w") as file:
        file.write(a+b)

#while true 获得状态
def sendstatus(Serial,Dtime,Otime,Btime,Stime,f):
    start_time = time.time()
    end_time =time.time()
    send_time=Stime
    ifreboot='0'
    ifoutput='0'
    ifend=0
    # classnum=random.randint(1,3)
    classnum=0
    data_cache=[]

    while end_time - start_time <= Dtime:
        #整数判断
        end_time=time.time()
        single_sen(slist[i], data_cache)
        if end_time-start_time >send_time:#分类结果之后的时间


            classnum=getclassnum(data_cache)
            ifreboot=getreboot(start_time,end_time,Otime,Btime)
            ifoutput=getoutput(start_time,end_time,Otime,classnum)
            refresh_status(ifreboot,ifoutput,f)
            send_time+=Stime
            if ifreboot=='1':
                ifend=1
                break
    if ifend==0:
        refresh_status('1',ifoutput,f)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = "status.txt"     #保存的文件地址
    duration_time=45     #分类极限时间，超过会shutdown
    output_time=15
    blow_max=30   #吹扫极限时间
    blow_min=10   #吹扫最短时间
    send_time=0.5   #2Hz频率
    blow_time=random.randint(blow_min, blow_max)

    S1 = Serialclass("/dev/tty.usbmodem142101", 'dzb1', 1)
    # blow_time=duration_time-output_time
    sendstatus(S1,duration_time,output_time,blow_time,send_time,f)



