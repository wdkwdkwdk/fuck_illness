# coding:utf-8
import urllib
from bs4 import BeautifulSoup
import pymysql.cursors
import sys
import Queue
import threading
import re
import time
reload(sys)
sys.setdefaultencoding('utf8')



def getHtml(url):
    # 获取网页内容
    page = urllib.urlopen(url)
    html = page.read()
    return html

def get_info(html):
	soup = BeautifulSoup(html)
	text = soup.find('div','g-under-askT').find_all('span')[0].get_text()
	time = text.strip() 
	text = soup.find('div','g-under-askB').find_all('span')[0].get_text()
	sex = text
	text = soup.find('div','g-under-askB').find_all('var')[0].get_text()
	age = text
	age = age.replace('年龄','')
	age = age.replace('岁','')
	age = age.replace('：','')
	title = soup.find('div','g-under-askT').find_all('h1')[0].get_text()
	info = soup.find('p','crazy_keyword_inlink').get_text()
	# answer = soup.find('div','g-otherask-b article-cont').find_all('div','g-under-askB')[0].get_text()
	#answer = re.sub('\n','',answer)
	drugs = soup.find('div','g-otherask-b article-cont').find_all('p','crazy_keyword_inlink')
	answer = ''
	for i in drugs:
		answer = answer + i.get_text()
	answer = re.sub('\n','',answer)
	data={}
	data['time'] = time
	data['sex'] = sex
	data['age'] = age
	data['title'] = title
	data['info'] = info
	data['answer'] = answer
	return data



def add_data(data,iid):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	# 使用 execute()  方法执行 SQL 查询 
	sql = "INSERT INTO fuck_ill(age,sex,time,ill_detail,doctor_answer,title,ill_id) VALUES('"+data['age']+"','"+data['sex']+"','"+data['time']+"','"+data['info']+"','"+data['answer']+"','"+data['title']+"','"+iid+"')"
	cursor.execute(sql)
	cursor.close()

def do_scan(ill_id):
	x_s = str(ill_id)
	res = getHtml('https://m.120ask.com/askg/posts_detail/'+x_s)
	try:
		results = get_info(res)
	except Exception as e:
		pass
	else:
		try:
			add_data(results,x_s)
		except pymysql.InternalError    as e:
			pass
		else:
			pass
		pass

	
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

def scan():
	while not q.empty():
		ill_id = q.get()
		do_scan(ill_id)
		


def worker():
	while not q.empty():
		#print(threading.activeCount())
		ill_id = q.get()
		do_scan(ill_id)
		time.sleep(1) 
	
		
a = check_state()
newest =  a[0]['ill_id']
goal = newest + 500000

q = Queue.Queue()
for x in range(newest,goal):
	q.put(x)



for i in xrange(50):
	t = threading.Thread(target=worker)
	t.setDaemon(True)
	t.start()

while True:
        if threading.activeCount() <= 1 :
            break
        else:
            try:
                time.sleep(1)
            except KeyboardInterrupt, e:
                print '\n[WARNING] User aborted, wait all slave threads to exit, current(%i)' % threading.activeCount()
                exit()

