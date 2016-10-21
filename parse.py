#coding:utf-8
from selenium import webdriver
import wx

######

#Python的线程池实现

import Queue
import threading
import sys
import time

#替我们工作的线程池中的线程
from tqdm import trange


class MyThread(threading.Thread):
    def __init__(self, workQueue, resultQueue,timeout=30, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
  #线程在结束前等待任务队列多长时间
        self.timeout = timeout
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.start()

    def run(self):
        while True:
            try:
    #从工作队列中获取一个任务
                callable, args, kwargs = self.workQueue.get(timeout=self.timeout)
    #我们要执行的任务
                res = callable(args, kwargs)
    #报任务返回的结果放在结果队列中
                self.resultQueue.put(" | ")
            except Queue.Empty: #任务队列空的时候结束此线程
                break
            except :
                print sys.exc_info()
        raise

class ThreadPool:
    def __init__( self, num_of_threads=10):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.threads = []
        self.__createThreadPool( num_of_threads )

    def __createThreadPool( self, num_of_threads ):
        for i in range( num_of_threads ):
            thread = MyThread( self.workQueue, self.resultQueue )
            self.threads.append(thread)

    def wait_for_complete(self):
  #等待所有线程完成。
        while len(self.threads):
            thread = self.threads.pop()
   #等待线程结束
            if thread.isAlive():#判断线程是否还存活来决定是否调用join
                thread.join()

    def add_job( self, callable, *args, **kwargs ):
        self.workQueue.put( (callable,args,kwargs) )

def test_job(id,sleep=0.001,str1='',str2=''):
    #print "start-->>"
    #browser = webdriver.Chrome('C:\Users\panda\Desktop\chromedriver.exe') # Get local session of firefox
    browser=webdriver.PhantomJS()
    #browser.get(r'http://pansijian.haodf.com/') # Load page
    browser.get(str1)
    browser.find_element_by_xpath("//a[@href='"+str2+"']").click()
    #print "get-->>"
    #time.sleep(0.5)
    '''
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_4665893517.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_4665890049.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_762003753.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_88090.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_117533.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_117532.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_117335.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_105293.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_88139.htm']").click()
    browser.find_element_by_xpath("//a[@href='http://www.haodf.com/zhuanjiaguandian/pansijian_728697605.htm']").click()
   '''
    #print "click-->>"
    #time.sleep(0.5) # Let the page load, will be added to the API
    browser.close()
    #browser.quit()

def test(str1='',str2=''):
    '''
    print "Instruction\n"
    print"please input the time that you want to click,and then you will see\n"
    print"how many times do you want to add  then you should input an Integer\n"
    print"then you will see start testing---->>>>and then the proceduce last for\n"
    print"several minutes so keep calm and wait for the 'end testing' then you can\n"
    print"close it"
    '''
    count=0
    #a=input("how many times do you want to add  ")
    print 'start testing'
    tp = ThreadPool(10)
    for i in range(500):
        time.sleep(0.2)
        tp.add_job( test_job, i, i*0.001,str1,str2 )
        count+=1
        #print "Click "+str(count)+" time(s) \n"
        #print "please wait for 'end testing'\n"
    tp.wait_for_complete()
    #print 'result Queue\'s length == %d '% tp.resultQueue.qsize()
    #print count
    while tp.resultQueue.qsize():
        print tp.resultQueue.get()
    #print 'end testing'

class MyFrame(wx.Frame):

    def __init__(self, parent=None, title=u'IC系统'):
        wx.Frame.__init__(self, parent, -1, title=title)
        self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)

        self.label1=wx.StaticText(self.panel,-1,label=u'主页面链接：')
        self.label2=wx.StaticText(self.panel,-1,label=u'点击网页链接：')
        self.userText=wx.TextCtrl(self.panel,-1,size=(200,25))
        self.passText=wx.TextCtrl(self.panel,-1,size=(200,25))

        self.gbsizer1=wx.GridBagSizer(hgap=10, vgap=10)
        self.gbsizer1.Add(self.label1,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        self.gbsizer1.Add(self.userText,pos=(0,1),span=(1,1),flag=wx.EXPAND)
        self.gbsizer1.Add(self.label2,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        self.gbsizer1.Add(self.passText,pos=(1,1),span=(1,1),flag=wx.EXPAND)

        self.loginBtn=wx.Button(self.panel,-1,label=u'开始绘图')
        self.loginBtn.Bind(wx.EVT_BUTTON,self.OnTouch)

        self.bsizer=wx.BoxSizer(wx.HORIZONTAL)
        self.bsizer.Add(self.loginBtn)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.gbsizer1, 0, wx.EXPAND, 20)
        self.sizer.Add(self.bsizer, 0, wx.EXPAND, 20)

        self.isShown = False    #用这个变量指示当前是否已将控件隐藏
        self.SetClientSize((330,118))    #更改面板尺寸
        self.panel.SetSizerAndFit(self.sizer)
        self.sizer.SetSizeHints(self.panel)

    def OnTouch(self, event):

#提取地区
#提取道路
        test(self.userText.GetValue(),self.passText.GetValue())
        '''
        可以在这里调用绘图程序
        下面这一段是一个弹出progress_bar的代码
        这段代码可以进行修改让它同步绘图过程
       '''
        progressMax = 100
        dialog = wx.ProgressDialog("A progress box", "Time remaining", progressMax,
            style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        keepGoing = True
        count = 0

        while keepGoing and count < progressMax:
            count = count + 1
            wx.Sleep(1)
            keepGoing = dialog.Update(count)#更新进度条进度

        dialog.Destroy()
        self.sizer.Layout()    #关键所在，强制sizer重新计算并布局sizer中的控件
 #处理结果
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()


####

