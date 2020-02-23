# -*- coding:utf-8 -*-
# 根据设备ID号进行指定设备进行操作
# 多线程控制多台设备
#####运行程序时请配置adb环境##  ##
import os
import sys
import threading
import time
import random
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

IDlist = []
# Swipe_X_start_point = 650 #滑动X起始点
# Swipe_Y_start_point = 1495 #滑动Y起始点
# Swipe_X_end_point = 611 #滑动X终点
# Swipe_Y_end_point = 1095  #滑动Y终点
def swipe_page(i):
    numcount=1
    CMD_device_size = 'adb -s {} shell wm size'.format(IDlist[i])
    sizeFile = os.popen(CMD_device_size)
    sizelist = sizeFile.readlines()
    # print(sizelist[0].split(':')[1].strip().split('x')[0]) #['Physical size: 1080x2340\n']
    device_X = sizelist[0].split(':')[1].strip().split('x')[0] # 1080
    device_Y = sizelist[0].split(':')[1].strip().split('x')[1] # 1920
    Swipe_X_start_point = int(int(device_X) * 0.6) #滑动X起始点
    Swipe_Y_start_point = int(int(device_Y) * 0.7) #滑动Y起始点
    Swipe_X_end_point = Swipe_X_start_point - 50 #滑动X终点
    Swipe_Y_end_point = Swipe_Y_start_point - 550  #滑动Y终点
    # CMD_tap = 'adb -s {} shell input tap 900 1795'.format(IDlist[i])
    CMD_toTop = "adb -s {} shell input swipe {} {} {} {}".format(IDlist[i],Swipe_X_start_point,Swipe_Y_start_point,Swipe_X_end_point,Swipe_Y_end_point) #模拟滑动桌面
    # print(CMD_tap)
    while(True):
        time.sleep(random.uniform(5,6))
        print("设备{}阅读了{}页,共耗时{:.2f}分钟".format(IDlist[i],numcount,numcount*5/60.00))
        string = "设备{}阅读了{}页,共耗时{:.2f}分钟".format(IDlist[i],numcount,numcount*5/60.00)
        # text.insert(END,"{}\n".format(string))
        # text.see(END)
        # text.update()
        try:
            os.system(CMD_toTop)
            numcount+=1
        except Exception as e:
            print("Error: ",e)

def get_devices_ID():
    CMD = 'adb devices'
    os.system(CMD)
    connectfile = os.popen(CMD)
    # print(type(connectfile))
    list = connectfile.readlines()
    # print(list)
    for i in range(len(list)):
        if list[i].find('\tdevice') != -1:
            ID = list[i].split('\t')[0]
            print(ID)
            IDlist.append(ID)
    print("当前连接设备数为:{}".format(len(IDlist)))
    string = "当前连接设备数为:{}".format(len(IDlist))
    text.insert(END,"{}\n".format(string))
    text.see(END)
    text.update()
    return IDlist

def threadsFunc():
    threadslist = []
    get_devices_ID()
    for i in range(len(IDlist)):
        thread = threading.Thread(target=swipe_page,args=(i,))
        threadslist.append(thread)
        thread.start()
    for eachthread in threadslist:
        eachthread.join()

def threadsEnd():
    if messagebox.askokcancel('Quit','Do you want to quit?'):
        root.quit()
    
    
if __name__ == "__main__":
    root = Tk()
    root.title("批量刷短视频神器")
    # root.geometry('300x200')
    root.geometry('300x200')
    root.resizable(width=False,height=False)
    # varl = StringVar()
    text = ScrolledText(root,font=('Aroal',13))
    text.place(x=10,y=30,width=280,height=130)
    # text = ScrolledText(root,x=10,y=30,width=680,height=450)

    button_start = Button(root,text="START",font=('Arial',13),command=threadsFunc)
    button_start.place(x=50,y=162,width=200,height=38)

    # button_end = Button(root,text="END",font=('Arial',13),command=threadsEnd)
    # button_end.place(x=145,y=75,width=100,height=50)
    # root.protocol("WM_DELETE_WINDOW",threadsEnd)
    root.mainloop()
    # print(threadslist)
