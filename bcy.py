# -*-coding:utf8-*-

import requests
import json
import MySQLdb
from multiprocessing.dummy import Pool as ThreadPool
import sys
import datetime
import time
import re
from lxml import etree #引入xpath解析
import json
import threading,time
import os
import httplib
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

url = ['http://180.186.38.200/rest/n/feed/list?mod=Xiaomi(Redmi%20Note%203)&lon=NaN&country_code=CN&did=ANDROID_3946317879949895&app=0&net=WIFI&oc=WANDOUJIA_CPD&ud=346048378&c=XIAOMI&sys=ANDROID_5.1.1&appver=4.52.2.2746&language=zh-cn&lat=NaN&ver=4.52']

headers = {'Host': '180.186.38.200',
           'User-Agent': 'kwai-android',
           'Accept-Encoding': 'gzip',
           'Content-Type' : 'multipart/form-data'
           }

def GetNowTime():

    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def sqlExecute(sql,arge=None):
    try:
        conn = MySQLdb.connect(host='123.57.153.40', user='root', passwd='15811225474', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('bcy')
        cur.execute(sql,arge)

        cur.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def sqlQuery(sql,arge=None):
    try:
        conn = MySQLdb.connect(host='123.57.153.40', user='root', passwd='15811225474', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('bcy')
        return cur.execute(sql,arge)
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])





def get_list(url):

    response = requests.get( url, params=None)

    list = re.findall('<a href="/u/(.*?)" class="name">.*?</a>',response.text,re.S)

    for item in list:
        user_url = "http://bcy.net/u/"+item
        result = sqlQuery('select uid from user where uid ='+ item)
        if result:
            print '已录入'
            continue


        #获取个人页
        response_page = requests.get(user_url, params=None)
        gender =  re.findall('<i class="i-work-sex-30-0 posa avatar-sex"></i>', response_page.text, re.S)
        fans_focus = re.findall('<p class="fz18 mb5">(.*?)</p>', response_page.text, re.S)

        if re.findall('<span class="gouda--tag fz12">(.*?)</span>', response_page.text, re.S):
            gouda = re.findall('<span class="gouda--tag fz12">(.*?)</span>', response_page.text, re.S)[0]
        else:
            gouda = 0


        if re.findall('<a class="l-left mr5 fz22 text-shadow lh28 _white text-shadow" .*?>(.*?)</a>', response_page.text, re.S):
            name = re.findall('<a class="l-left mr5 fz22 text-shadow lh28 _white text-shadow" .*?>(.*?)</a>', response_page.text, re.S)[0]
        else:
            name = '未命名'

        gender = 0 if gender else 1
        fans = fans_focus[0]
        focus = fans_focus[1]
        praise  = re.findall('<span class="red">(.*?)</span>', response_page.text, re.S)[0]
        publish_count = re.findall('<span class="red fz18 vab">(.*?)</span>', response_page.text, re.S)[0]
        address = re.findall('<span class="fz14">(.*?)</span>', response_page.text, re.S)[0]

        values =[name,gender,fans,focus,gouda,praise,publish_count,address,item]


        sqlExecute('insert into user (name,gender,fans,focus,gouda,praise,publish_count,address,uid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   (name,gender,fans,focus,gouda,praise,publish_count,address,item))
        print '写入一条数据'


def run(page,sec):

    for i in range(page[0],page[1],1):
        print '当前线程'+page[2]+'为开始页为'+str(page[0])+'当前页为'+str(i)+'结束页为'+str(page[1])
        get_list('http://bcy.net/coser/allwork?&p='+str(i))

if __name__ == '__main__':
    pages = [[1, 500,'线程1'],
             [500, 1000,'线程2'],
             [1000, 1500,'线程3'],
             [1500, 2000,'线程4'],
             [2000, 2500,'线程5'],
             [2500, 2690,'线程6']
             ]
    threadpool = []
    for page in pages:
        th = threading.Thread(target=run, args=(page, 2))
        threadpool.append(th)

    for th in threadpool:
        th.setDaemon(True)
        th.start()
    th.join()
