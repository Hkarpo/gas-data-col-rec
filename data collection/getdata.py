import serial
import time
from makeandwrite import *
import winsound
duration = 1000  # millisecond
freq = 440  # Hz

from serialclass import *


def update(start_time,end_time,duration,slist,write_time):
    dataall=[]
    create_father_list(dataall,len(slist))
    j_time=write_time

    while end_time - start_time <= duration:
        print(end_time - start_time)
        end_time = time.time()
        for i in range(len(slist)):
            slist[i].openbeng()

            dataload=dataall[i]

            if slist[i].title=="环境":
                env_sen(slist[i],dataload)

            else:
                single_sen(slist[i],dataload)

        if (end_time - start_time>j_time):
            print("已进行时间:%d"%(end_time - start_time)+'秒')
            print("正在写入数据")
            # k=single_sen[-1][1:16]
            # print(k)
            #
            writeall(slist, dataall)
            ser_flush_all(slist)
            data_clear(dataall)
            j_time+=write_time
    print("数据计入结束")
    writeall(slist, dataall)
    winsound.Beep(freq, duration)


def single_sen(S,dataload):
    d = time.localtime()
    cur_time1 = time.strftime('%m.%d.%H%M%S', d)
    try:
        value = S.get_raw_data()
        dataArray = value.split(',')
        dataArray[-1]=float(dataArray[-1])
        # print(dataArray)
    except(ValueError, PermissionError):
        ser_flush_all(S)
        dataArray = []
        print("串口问题报错", cur_time1)
        for c in range(19):
            dataArray.append('nan')
    dataload.append([cur_time1] + dataArray)

def env_sen(S,dataload):
    d = time.localtime()
    cur_time1 = time.strftime('%m.%d.%H%M%S', d)
    try:
        value = S.get_raw_data()
        dataArray = value.split(',')
        # print(dataArray)
        # print(dataArray)
    except(ValueError, PermissionError):
        ser_flush(S)
        dataArray = []
        print("串口问题报错", cur_time1)
        for c in range(2):
            dataArray.append('nan')
    dataload.append([cur_time1] + dataArray[:2])

if __name__=='__main__':
    base_dir = os.path.dirname(__file__)
    print(base_dir)
    start_time = time.time()
    end_time = time.time()

    #修改以下
    #板子及数量修改
    #注意在slist中新增加S”X“


    #S4 = Serialclass("COM33","空_1121")
    #S4 = Serialclass("COM33", "白酒_1118")
    #S4 = Serialclass("COM33", "白醋_1118")
    #S4 = Serialclass("COM33", "白酒+白醋_1118")
    #S4 = Serialclass("COM33","白酒+酱油_1118")
    #S4 = Serialclass("COM33","酱油+白醋_1118")
    S4 = Serialclass("COM33","柠檬_1123")

    S4.ser.write("0".encode())
    # print("???")
    slist=[S4]
    #时间部分修改

    duration = timecount(0, 0, 1, 30)  # 持续时间(天数,小时数,分钟,秒) 17小时
    write_time = timecount(0, 0, 1, 30)  # 记录数据时间20min


    #修改结束
    #注：波特率与文件路径在makedir函数和serial类里面修改


    print('持续时间:%d' % duration + '秒' + "  " + '写入间隔:%d' % write_time + '秒')
    update(start_time,end_time,duration,slist,write_time)
    print("检测结束")

