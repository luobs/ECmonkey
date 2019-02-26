#-*- coding: utf-8 -*-
#Author : liaozhenyang

import os
import time

packageName = "com.eclite.activity"
path=os.path.abspath('.')

devicesfile = r'\devices.log'
logcatfile = r'\logcat.log'
tracesfile = r'\traces.log'

filepath = path+devicesfile
file = open(filepath,'w')
file.write('')
file.close()

os.system('adb shell cat /system/build.prop > %s'%filepath)


def getDeviceInfo(path):
    f = open(path,"r",encoding="UTF-8")
    lines = f.readlines()
    for line in lines:

        line=line.split('=')
        if (line[0]=='ro.build.version.release'):
            version = line[1]
        if (line[0]=='ro.product.model'):
            model = line[1]
        if (line[0]=='ro.product.brand'):
            brand = line[1]
    return version,model,brand


def monkeyRun(count):
    """
    monkey test
    :param count: 总事件次数
    :param throttle: 事件间隔(ms)
    :param pct-touch: touch事件
    :param pct-motion: 滑动事件
    :param pct-nav: 导航事件
    :param pct-majornav: 主导航事件
    :param pct-appswitch: 切换activity事件
    :param pct-anyevent: 其他事件
    :param pct-trackball : 轨迹球事件
    :param pct-syskeys : 系统按键
    :param other: 未指定的剩余事件
    :return: Monkeylog
    """
    #删除monkey.log
    os.remove(filepath)
    
    print ("----使用Logcat清空Phone中log")
    os.system("adb logcat -c")
    time.sleep(2)
    
    now1 = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    monkeylogname=path+"\\"+now1+"_monkey.log"
    #print monkeylogname
    #分配事件：点击事件30%，滑动事件20%，导航20%,主导航15%,切换activity事件5%,其他事件5%，轨迹球事件0%,系统按键0%.
    throttle = 300
    touch = 30
    motion = 20
    nav = 20
    majornav = 15
    appswitch = 5
    anyevent = 5
    trackball = 0
    syskeys = 0

    cmd="adb shell monkey -v -v -p %s -s 500 --ignore-timeouts --ignore-native-crashes --throttle %d --pct-touch %d " \
        "--pct-motion %d --pct-nav %d --pct-majornav %d --pct-appswitch %d --pct-anyevent %d --pct-trackball %d --pct-syskeys %d " \
        "-v -v %d >>%s"\
        %(packageName,throttle,touch,motion,nav,majornav,appswitch,anyevent,trackball,syskeys,int(count),monkeylogname)
    
    print("----开始执行Monkey命令")
    os.system(cmd)   
    
    print("----手机截屏")
    os.system("adb shell /system/bin/screencap -p /sdcard/monkey1.png")
    oldname=path+"\\"+r"_monkey1.png"
    if (os.path.exists(oldname)):
        print ("----替换已存在截图")
        newname=path+"\\"+now1+r"_monkey2.png"
        os.rename(oldname, newname)
    else:
        pass
        #print "file isn't exist"
        
    # print"----拷贝截屏图片至电脑"
    # cmd1="adb pull /sdcard/monkey.png %s" %(path)
    # os.system(cmd1)
    
    print("----使用Logcat导出日志" )
    logcatname=path+"\\"+now1+r"_logcat.log"
    cmd2="adb logcat -v time -d >%s" %(logcatname)
    os.system(cmd2)
    
    print("----导出Traces日志")
    tracesname=path+"\\"+now1+r"_traces.log"
    cmd3="adb shell cat /data/anr/traces.txt>%s" %(tracesname)
    os.system(cmd3)
    return monkeylogname,logcatname,tracesname
    
