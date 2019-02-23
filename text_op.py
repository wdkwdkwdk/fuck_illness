# ecoding=utf-8
#这个脚本实现功能为，把纯文本语料库xuewei.txt转化成jieba分词和词频统计的字典，分别为dic_for_use和dic_for_use
ifn = r"xuewei.txt"
ofn = r"dic_for_idf.txt"
ofn2 = r"dic_for_use.txt"
infile = open(ifn,'rb')
outfile = open(ofn,'wb')
outfile2 = open(ofn2,'wb')

for eachline in infile.readlines():
        lines = eachline.strip()
        lines1 = lines+' 100\n'
        lines2 = lines+' 100 n\n'
        outfile.write(lines1)
        outfile2.write(lines2)

infile.close
outfile.close
outfile2.close