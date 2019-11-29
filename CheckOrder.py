#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import time
from wxpy import *
import requests
import random
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CheckOrder(QObject):
    AlertSignal = pyqtSignal(str)
    def __init__(self):
        super(CheckOrder, self).__init__()
        # 信号源账户信息

        self.SourceAccountList = [2090463533,55864420]
        self.SourceAccountCurOrders = {};
        #跟单账户信息
        self.SlaveAccountList = [4002645,4002649,51191958,4002651]
        self.NewOpenTicket = {};
        self.NewCloseTicket ={};
        self.TargetName="少先队员"
        self.CheckNewOrderTime=time.time();
        self.CheckSlaveOrderTime=time.time();
        self.SendMailBool=False
    def InitCurOrders(self,accountid):
        self.db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        self.cursor =  self.db.cursor()
        self.cursor.execute("SELECT OrderTicket from posorders.%s" % accountid)
        self.data = self.cursor.fetchall()
        list = []
        for row in self.data:
            list.append(row[0])
        self.SourceAccountCurOrders[accountid] = list
        self.db.close()
    def SearchNewOrders(self,accountid):
        db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        cursor = db.cursor()
        cursor.execute("SELECT OrderTicket from posorders.%s where OrderType = 1 or ordertype = 0" % accountid)
        data = cursor.fetchall()
        ticket = []
        contents = ""
        for row in data:
            ticket.append(row[0])
        if ticket != self.SourceAccountCurOrders[accountid]:
            if len(ticket) > len(self.SourceAccountCurOrders[accountid]):
                for i in ticket:
                    if i not in self.SourceAccountCurOrders[accountid]:
                        cursor.execute("SELECT * from posorders.%s where OrderTicket = %s" % (accountid,i))
                        data = cursor.fetchone()
                        ticketid = data[0]
                        self.NewOpenTicket[ticketid]=self.SlaveAccountList.copy()
                        symbol = data[1]
                        type = "买" if data[2]==0 else "卖"
                        lots = data[3]
                        price = data[9]
                        contents = "%s\n信号源: %s\n开仓: %s\n货币: %s\n方向: %s\n手数: %s\n价格:%s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),accountid,ticketid,symbol,type,lots,price)
                        print(contents)
                        if self.SendMailBool:
                            self.SendAlert(self.TargetName, contents)
                        self.AlertSignal.emit(contents)
                        self.SourceAccountCurOrders[accountid].append(i)
            if len(ticket) < len(self.SourceAccountCurOrders[accountid]):
                for i in self.SourceAccountCurOrders[accountid]:
                    if i not in ticket:
                        cursor.execute("SELECT * from hisorders.%s where OrderTicket = %s" % (accountid, i))
                        data = cursor.fetchone()
                        ticketid = data[0]
                        self.NewCloseTicket[ticketid]=self.SlaveAccountList.copy()
                        symbol = data[1]
                        type = "买" if data[2] == 0 else "卖"
                        lots = data[3]
                        price = data[11]
                        profit = data[14]
                        contents = "%s\n信号源: %s\n平仓: %s\n货币: %s\n方向: %s\n手数: %s\n价格:%s\n盈利: %s" % (
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), accountid, ticketid, symbol, type,
                        lots, price,profit)
                        print(contents)
                        if self.SendMailBool:
                            self.SendAlert(self.TargetName, contents)
                        self.AlertSignal.emit(contents)
                        self.SourceAccountCurOrders[accountid].remove(i)
        db.close()
    def SendAlert(self,name = "",contents = ""):
    #return 0;
        try:
            my_friend = bot.search(name)[0]
            my_friend.send(contents)
        except:
            my_friend = bot.search('X-Trader')[0]
            my_friend.send(u"消息发送失败")
    def SearchFollowOpenOrders(self,openticket):
        contents = ""
        if openticket !=None:
            for key in list(openticket.keys()):
                ticketlist = []
                for i in openticket[key]:
                    db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
                    cursor = db.cursor()
                    cursor.execute("SELECT OrderComment from posorders.%s order by OrderOpenTime desc" % i)
                    data = cursor.fetchall()
                    for row in data:
                        if key in row[0]:
                            ticketlist.append(i)
                            break
                    cursor.close()
                    db.close()
                for ticket in ticketlist:
                    openticket[key].remove(ticket)
                if openticket[key] !=[]:
                    contents = u"信号源订单 %s 已跟单 %s，剩余 %s！" % (key,len(self.SlaveAccountList)-len(openticket[key]),len(openticket[key]))
                    print(contents)
                    self.AlertSignal.emit(contents)
                    if self.SendMailBool:
                        self.SendAlert(self.TargetName,contents)
                else:
                    del openticket[key]
                    contents = "信号源订单 %s 已全部跟单完成！" % key
                    print(contents)
                    self.AlertSignal.emit(contents)
                    if self.SendMailBool:
                        self.SendAlert(self.TargetName, contents)
    def SearchFollowCloseOrders(self,closeticket):
        contents = ""
        if closeticket != None:
            for key in list(closeticket.keys()):
                ticketlist = []
                for i in closeticket[key]:
                    db = pymysql.connect("localhost", "root", "Lianrun!@#", "hisorders")
                    cursor = db.cursor()
                    cursor.execute("SELECT OrderComment from hisorders.%s order by OrderCloseTime desc limit 10" % i)
                    data = cursor.fetchall()
                    for row in data:
                        if row[0]!=None:
                            if key in row[0]:
                                ticketlist.append(i)
                                break
                    cursor.close()
                    db.close()
                for ticket in ticketlist:
                    closeticket[key].remove(ticket)
                if closeticket[key]!=[]:
                    contents = "信号源订单 %s 已平单 %s，剩余 %s！" % (key, len(self.SlaveAccountList) - len(closeticket[key]), len(closeticket[key]))
                    print(contents)
                    self.AlertSignal.emit(contents)
                    if self.SendMailBool:
                        self.SendAlert(self.TargetName, contents)
                else:
                    del closeticket[key]
                    contents = "信号源订单 %s 已全部平仓完成！" % key
                    print(contents)
                    self.AlertSignal.emit(contents)
                    if self.SendMailBool:
                        self.SendAlert(self.TargetName, contents)
if __name__ == "__main__":
    bot = Bot(cache_path=True)
    checkinstance = CheckOrder()
    for account in checkinstance.SourceAccountList:
        checkinstance.InitCurOrders(account)
    while 1:
        #检查信号源新订单
        if time.time()-checkinstance.CheckNewOrderTime>=2:
            CheckNewOrderTime=time.time()
            #print(CheckNewOrderTime)
            for account in checkinstance.SourceAccountList:
                checkinstance.SearchNewOrders(account)
            #print(NewOpenTicket)
        #检查跟单账户跟单状态
        if time.time()-checkinstance.CheckSlaveOrderTime>=5:
            checkinstance.CheckSlaveOrderTime=time.time()
            checkinstance.SearchFollowOpenOrders(checkinstance.NewOpenTicket)
            checkinstance.SearchFollowCloseOrders(checkinstance.NewCloseTicket)
            #print(CheckSlaveOrderTime)
        #检查
    embed()