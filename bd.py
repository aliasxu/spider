#!/usr/bin/env python
#_*_ coding:utf-8 _*_
"""bd.py is an spider to baidu tieba NBATOP50"""

import urllib
import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")



#处理页面多余标签
class Tool:
    #去除img标签，7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行标签替换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将制表符<td>替换为\t
    replaceTD = re.compile('<td>')
    #把段落开头换为\n将两个空格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,'\n',x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()

class BDTB:

    #初始化，传入基地址，是否只看楼主参数
    def __init__(self,baseUrl,seeLZ,floorTag):
        #base地址
        self.baseURL = baseUrl
        #是否只看楼主，1为只看楼主，0为取消只看楼主
        self.seeLZ = '?see_lz='+str(seeLZ)
        #HTML标签剔除工具类对象
        self.tool = Tool()
        #全局file变量,文件写入操作对象
        self.file = None
        #楼层号
        self.floor = 1
        #默认标题，如果没有成功获取到标题的话则会使用这个标题
        self.defaultTitle = u'百度贴吧'
        #是否写入楼分隔标记符
        self.floorTag = floorTag

    #获取指定页的源码
    def getPage(self,pageNum):
        try:
            #构建URL
            url = self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u'连接百度贴吧失败，错误原因：',e.reason
                return None

    #获取帖子标题
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

    #获取帖子一共有多少页
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            # print  result.group(1)  #测试输出
            return result.group(1)
        else:
            return None

    #获取每一楼的内容
    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = '\n'+self.tool.replace(item)+'\n'
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + '.txt','w+')
        else:
            self.file = open(self.defaultTitle + '.txt','w+')


    def writeData(self,contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = '\n' + str(self.floor) + u"楼" + '---'*30
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum()
        title = self.getTitle()
        self.setFileTitle(title)
        if pageNum == None:
            print 'URL已经失效'
            return None
        try:
            print '该帖子共有'+ str(pageNum) + '页'
            for i in range(1,int(pageNum)+1):
                print "正在写入第%d页数据" %i
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError,e:
            print '写入异常，原因：'+ e.message
        finally:
            print '写入任务完成'



baseURL = raw_input("请输入帖子的url：")
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0：")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0：")
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()