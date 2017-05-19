#!/usr/bin/env python
#_*_ coding:utf-8 _*_
"""抓取淘宝mm"""

import urllib
import urllib2
import re
import os
import tool

class TBSpider:

    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

    #获取页面的源码
    def getPage(self,pageIndex):
        url = self.siteURL + '?page=' + str(pageIndex)
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    #获取索引页所有MM的信息，list格式
    def getContent(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="list-item">.*?s60">.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
                             re.S)
        items = re.findall(pattern,page)
        contents=[]
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents

    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')

    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        return self.tool.replace(result.group(1))

    #获取页面所有图片
    def getAllImg(self,page):
        pattern =re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern,page)
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(patternImg,content.group(1))
        return images

    #保存多张写真图片
    def saveImgs(self,images,name):
        number = 1
        print u'发现',name,u'共有',len(images),u'张照片'
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = 'jpg'
            filename = name + '/' + str(number)+'.'+fTail
            self.saveImg(imageURL,filename)
            number += 1

    #保存头像
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        filename = name + '/icon.' + fTail
        self.saveImg(iconURL,filename)

    #保存个人简介
    def saveBrief(self,content,name):
        filename = name + '/' + name + '.txt'
        f = open(filename,'w+')
        print u'正在保存她的个人信息为：',filename
        f.write(content.encode('utf-8'))

    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,filename):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(filename,'wb')
        f.write(data)
        print '正在保存她的图片：',filename
        f.close()


    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        ifExists = os.path.exists(path)
        if not ifExists:
            print "正在创建文件夹：",path
            os.makedirs(path)
            return True
        else:
            return False

    #将第一页MM的信息保存起来
    def savePageInfo(self,pageIndex):
        contents = self.getContent(pageIndex)
        for item in contents:
            #item[0]个人详情URL，item[1]头像URl，item[2]姓名，item[3]年龄,item[4]居住地
            print u'发现一位模特，名字叫%s,芳龄：%s,她在%s' %(item[2],item[3],item[4])
            print u"正在保存%s的信息" % item[2]
            print u'又意外的发现了她的主页：%s' % 'https:'+item[0]
            #个人详情页面URL
            detailURL = 'https:' + item[0]
            #获取个人详情页面代码
            detailPage = self.getDetailPage(detailURL)
            #获取个人信息
            brief = self.getBrief(detailPage)
            #获取所有图片列表
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            #保存个人简介
            self.saveBrief(brief,item[2])
            #保存头像
            self.saveIcon(item[1],item[2])
            #保存图片
            self.saveImgs(images,item[2])

    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u'正在保存第',i,u'地方，看MM们在不在'
            self.savePageInfo(i)


tb = TBSpider()
tb.savePagesInfo(2,10)