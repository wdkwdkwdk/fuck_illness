# coding:utf-8
import urllib
from bs4 import BeautifulSoup
import pymysql.cursors
import sys
import Queue
import threading
import re
import subprocess
import os
import time
reload(sys)
sys.setdefaultencoding('utf8')




def check_state():
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	# 使用 execute()  方法执行 SQL 查询 
	sql = "select * from fuck_ill where 1 order by ill_id desc limit 1"
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	return results
	


a = check_state()
newest =  a[0]['ill_id']
time.sleep(3)
print('the newest id is:'+str(newest))

while True:
	a = check_state()
	new =  a[0]['ill_id']
	if((new-newest)<20):
		print('ready to restart health')
		try:
			std.kill()
		except Exception as e:
			print(e)
			print('kill std fail')
		else:
			print('kill std sucess')
		std = subprocess.Popen('python health.py')
	else:
		how = int(new) - int(newest)
		how = str(how)
		newest = new
		print('fetch '+how+' datas in the last 5 seconds')
	time.sleep(5)


