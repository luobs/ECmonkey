#-*- coding: utf-8 -*-
#Author : liaozhenyang

######################
#error
######################
import time,os,re
import threading,traceback
from MonkeyExec import getDeviceInfo, monkeyRun
NullPointer="java.lang.NullPointerException"
IllegalState="java.lang.IllegalStateException"
IllegalArgument="java.lang.IllegalArgumentException"
ArrayIndexOutOfBounds="java.lang.ArrayIndexOutOfBoundsException"
RuntimeException="java.lang.RuntimeException"
SecurityException="java.lang.SecurityException"
crashException=""
#System.err = "System.err"
ExceptionList = {
    NullPointer:"java.lang.NullPointerException",
    IllegalState:"java.lang.IllegalStateException",
    IllegalArgument:"java.lang.IllegalArgumentException",
    ArrayIndexOutOfBounds:"java.lang.ArrayIndexOutOfBoundsException",
    RuntimeException:"java.lang.RuntimeException",
    SecurityException:"java.lang.SecurityException"
}

logdir=os.path.abspath('.') + '\devices.log'
#logdir = '/Users/mac/Desktop/monkey_log/monkey.log'
now1 = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
version,model,brand=getDeviceInfo(logdir)

#print"Monkey"
global logs
def getlog(count):
    global logs
    logs=monkeyRun(count)
    logs = list(logs)

def relog(log,fr,strtype):
    global count
    global crashlist
    cc = 0
    try:
        # with open(log, 'rb') as fb:
        #     lines = fb.readlines()
        #     for line in lines:
        #         line = line.decode(strtype).strip("\r\n")
        #         Strlines.append(line)
        with open(log,'rb') as f:
            lines = f.readlines()
            print ("----遍历 <%s>"%log)
            for line in lines:
                #将二进制line编码为字符串，不然无法进行正则匹配
                sline = line.decode(strtype).strip("\r\n")
                if (re.findall(NullPointer, sline) or re.findall(IllegalState, sline) or re.findall(IllegalArgument,sline) or re.findall(ArrayIndexOutOfBounds, sline) or re.findall(RuntimeException, sline) or re.findall(SecurityException,
                                                                                                                                                                                                                           sline)):
                    a = lines.index(line)
                    print ('the umber is:%d' %(a + 1))
                    count += 1
                    cc += 1
                    if "E/CrashHandler" in sline:
                        crashlist.append(sline)
                    for var in range(a, a + 1):
                        print (lines[var])
                        fr.write('at %s:%d' %(log,a))
                        fr.write('\n')
                        fr.write(lines[var].decode(strtype).strip("\r\n"))
                        fr.write("\n")
                else:
                    continue
    except Exception as e:
        #print(traceback.print_exc())
        pass
    if cc == 0:
        print ("pass")
    #print(set(crashlist))
    return count,len(set(crashlist))
def geterror():
    global logs
    global count
    global crashlist
    time.sleep(3)
    monkey = logs[0]
    logcat = logs[1]
    traces = logs[2]
    
    loglist = [r"{}".format(monkey),r"{}".format(logcat),r"{}".format(traces)]
    #loglist = [r"{}".format(logcat)]
    errfile = os.path.abspath('.') + "\\" + "error.log"
    if (os.path.exists(logdir)):
        os.remove(logdir)
    elif (os.path.exists(errfile)):
        os.remove(errfile)
    elif (os.path.exists(errfile)):
        os.remove(errfile)

    with open(errfile, 'w') as fr:
        fr.write('Version:' + version)
        fr.write("\n")
        fr.write('model:' + model)
        fr.write("\n")
        fr.write('brand:' + brand)
        fr.write("\n")
        fr.write("=" * 20)
        fr.write("\n")
        count = 0
        crashlist = []
        for log in loglist:
            try:
                count,crash = relog(log,fr,"UTF-8")
                if count is False:
                    count,crash = relog(log,fr,"gbk")

            except Exception as e:
                print(traceback.print_exc())
        if count == 0 or count == "False":
            os.remove(monkey)
            os.remove(logcat)
            os.remove(traces)
        print ('----log错误数量为:',count)
        print ('----crash数量为:',crash)

if __name__ == "__main__":
    count = input("please input run_monkey count:")
    t1 = threading.Thread(target = getlog, args = (count,))
    t1.setDaemon(True)
    t1.start()
    if t1.isAlive():
        t1.join()
        print ('----等待处理log...')
    geterror()
