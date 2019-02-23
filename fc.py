# encoding=utf-8
import time
import json
from wordcloud import WordCloud
import jieba
import jieba.analyse
from wordcloud import WordCloud, STOPWORDS
import pymysql.cursors
from scipy.misc import imread
#初始化开始时间，分词字典，词频统计字典
firsttime = time.time()
jieba.analyse.set_idf_path('dic_for_idf.txt')
jieba.set_dictionary('dic_for_use.txt')


def check_state(id = '12'):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    start = time.time()
    #此处SQL按需修改
    #sql = "select doctor_answer from fuck_ill where id>"+id+" order by ill_id asc limit 100000"
    sql = "select doctor_answer from fuck_ill where age>60"
    cursor.execute(sql)
    results = list(cursor.fetchall())
    end1 = time.time()
    es = end1 - start
    print('数据库第一步耗时：'+str(es))
    start = time.time()
    #解决编码问题
    line = results.__str__()
    line = line.decode('unicode_escape')
    #for循环效率很低，感兴趣的可以试试看为什么
    # for row in results:
    #     ill_detail = row['doctor_answer']
    #     line = line + ill_detail
    cursor.close()
    end1 = time.time()
    es = end1 - start
    print('数据库第二步耗时：' + str(es))
    return line

tongji = {}
def analyse(content):
    try:
        # jieba.analyse.set_stop_words('你的停用词表路径')
        global tongji
        tags = jieba.analyse.extract_tags(content, topK=200, withWeight=True)
        for v, n in tags:
            # 权重是小数，为了凑整，乘了一万
            if u'' + v in tongji:
                tongji[u'' + v] = tongji[u'' + v] + int(n * 10000)
            else:
                tongji[u'' + v] = int(n * 10000)
    finally:
        pass


#要分析多少行数据，在这里写，配合SQL语句使用
for x in range(12, 100000, 100000):
    start = time.time()
    content = check_state(str(x))
    end = time.time()
    escape = end - start
    print('本次数据库读取时间：' + str(escape))

    start = time.time()
    analyse(content)
    end = time.time()
    escape = end - start
    print('本次词频提取用时：' + str(escape))
    print 'do a work'
#此处也可以直接打印结果
#result = sorted(tongji.items(), key = lambda x: x[1], reverse=True)
#fre = json.dumps(result, ensure_ascii=False, encoding='UTF-8')
#绘制词云图
wordcloud = WordCloud(font_path = "simfang.ttf",background_color = 'White').generate_from_frequencies(tongji)
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
end = time.time()
escape = end - firsttime
print('总耗时：'+str(escape))