import csv
import os
import time
def writetitle(fp):
    with open(fp, "a", newline='') as f:
        headers = ["Time", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16","S17","S18","NOX", "VOCRAW", "CO2", "TVOC","TEM","HUM"]
        writer = csv.writer(f, delimiter=",")
        writer.writerow([i for i in headers])
def writefile(fp, data):
    with open(fp, "a", newline='') as f:
        writer = csv.writer(f, delimiter=",")
        for i in data:
             writer.writerow(i)
        f.close()
def writeenv(path,title,data):
    fp = getfilename(path, title)
    with open(fp, "a", newline='') as f:
        headers = ["Time","TEM", "HUM"]
        writert = csv.writer(f, delimiter=",")
        writert.writerow([i for i in headers])
        writerf = csv.writer(f, delimiter=",")
        for i in data:
            writerf.writerow(i)
        f.close()
    d = time.localtime()
    cur_time = time.strftime('%m.%d.%H%M%S', d)
    print(title + "环境写入完成时间:" + cur_time)
def makedir(dirname):
    # root="e:\\moredata\\518\\"
    # mkpath = root+dirname+"\\"
    mkpath=dirname
    # 调用函数
    mkdir(mkpath)
def mkdir(path):
    # path = path.strip()
    # path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False
def getfilename(path,title):
    d = time.localtime()
    cur_time = time.strftime('%m.%d.%H%M%S', d)
    name = './'+path +'/' +title + cur_time + ".csv"
    return name
def writemorefiles(path,title,data):
    fp=getfilename(path,title)
    with open(fp, "a", newline='') as f:
        headers = ["Time", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14",
                   "S15", "S16", "S17", "S18", "NOX", "VOCRAW", "CO2", "TVOC", "TEM", "HUM"]
        writert = csv.writer(f, delimiter=",")
        writert.writerow([i for i in headers])
        writerf = csv.writer(f, delimiter=",")
        for i in data:
             writerf.writerow(i)
        f.close()
    d = time.localtime()
    cur_time = time.strftime('%m.%d.%H%M%S', d)
    print(title+"组写入完成时间:"+cur_time)
def timecount(d,h,m,s):
    time=s+60*m+60*60*h+60*60*24*d
    return time
def writeall(slist,dataall):
    for i in range(len(slist)):
        dataload = dataall[i]
        # if i==len(slist)-1:
        if slist[i].title=="环境":
            # print("???")
            # env_sen(slist[i], dataload)
            # print(dataload)
            writeenv(slist[i].title, slist[i].title, dataload)
        else:
            # single_sen(slist[i], dataload)
            # print(slist[i])
            # k=dataload[0][1:17]
            # print("数据:",dataload[0])
            # print("预测：",predict_from_curdata(k))
            writemorefiles(slist[i].title, slist[i].title, dataload)
def create_father_list(dataall,num):
    for i in range(num):
        dataall.append([])
def data_clear(dataall):
    print('已清理缓存')
    for i in range(len(dataall)):
        dataall[i]=[]
def predict_from_curdata(X_input):
    mean = [3.4552176075603085, 1.3088435712509325, 0.20253916936085553, 2.0458119870678932, 1.7314125839343448,
            0.863775180303407, 3.361427505595623, 0.36788858492912213, 0.40028599850783386, 0.543305147973141,
            1.415861725938821, 0.989706540661527, 2.4296493409599598, 3.1344342203431985, 2.4563640885351905,
            2.6271300671474758]
    std=[0.4333613651057544, 0.5447422089958748, 0.15634756100142136, 0.7037627709443557, 0.7982452429699854,
         0.30849027598333323, 0.730380046765195, 0.10450172399221937, 0.2061204578611674, 0.238523589517658,
         0.6400894341732795, 0.2653915820020635, 0.6005030647350754, 0.33771863527293616, 1.3226439727232138,
         0.6248336821183659]
    model_c=[ -2.9533865 ,   0.50507307,  -2.48576956 ,  6.0421592 ,  -7.40874851,
  -4.486442    ,-2.29368788 , -4.4289661,    4.38916406  , 6.92532179,
  -2.53790045  , 3.89840449 ,  1.60060464  , 1.38827749  , 1.73921824,
 -10.90552524]
    model_i=33.2522250335718

    thispred=model_i
    if len(X_input)!=len(model_c):
        print(len(X_input))
        print("numprob")
    for i in range(len(X_input)):
        X1=(float(X_input[i])-mean[i])/std[i]
#         print(X1)
        thispred+=X1*model_c[i]
    return thispred