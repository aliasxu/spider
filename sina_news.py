#!/usr/bin/env python
#_*_ coding:utf-8 _*_
"""
sina_news.py is an spider for news.sina.com.cn
"""

import re
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

class SinaNewsSpider:

    def __init__(self,news_url):
        self.news_url = news_url
        self.news = {}
        self.news_title = []

    #获取网页源码
    def getPage(self,new_url = None):
        if new_url is None:
            res = requests.get(self.news_url)
        else:
            res = requests.get(new_url)
        res.encoding = 'utf-8'
        return res


    #获取最新消息
    def getNews(self):
        res = self.getPage()
        soup = BeautifulSoup(res.text,'html.parser')
        for new in soup.select('.news-item'):
            if len(new.select('h2')) > 0:
                title = new.select('h2')[0].text
                alink = new.select('a')[0]['href']
                time = new.select('.time')[0].text

                self.news[title] = {'alink':alink,'time':time}
                self.news_title.append(title)



    #获取新闻主要内容：新闻标题，新闻内容，编辑，发布时间，来源，评论数
    def getNewDetail(self,url):
        res = self.getPage(url)
        news_detail = {}
        soup = BeautifulSoup(res.text,'html.parser')

        #文章标题
        title = soup.select('#artibodyTitle')[0].text
        #文章发布时间
        timesource = soup.select('.time-source')[0].contents[0].strip()
        #来源
        source = soup.select('.time-source span a')[0].text

        #文章内容
        new_body= '\n'.join([ p.text.strip() for p in soup.select('#artibody p')[:-1]])

        #编辑
        editor = soup.select('.article-editor')[0].text

        #评论数
        comments = self.getComment(url)
        news_detail['title'] = title
        news_detail['timesource'] = timesource
        news_detail['source'] = source
        news_detail['new_body'] = new_body
        news_detail['editor'] = editor
        news_detail['comments'] = comments

        return news_detail

    #获取评论数
    def getComment(self,url):
        CommentUrl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
        s = re.search(r'doc-i(.*).shtml',url)
        new_id = s.group(1)
        res = self.getPage(CommentUrl.format(new_id))
        res = json.loads(res.text.strip('var data='))
        return res['result']['count']['total']



    #开始
    def start(self):
        print '正在获取sina最新消息，请稍等....'
        print "sina最新消息："
        self.getNews()
        for i,j in enumerate(self.news_title,1):
            print '%d:%s' %(i,j)
        choice = int(raw_input("which new do you want to see the tetail message: "))
        # print self.news_title[choice-1]
        # print self.news[self.news_title[choice-1]]['alink']
        news_detail = self.getNewDetail(self.news[self.news_title[choice-1]]['alink'])
        print 'New title:',news_detail['title']
        print 'New time:',news_detail['timesource']
        print '**New editor**:',news_detail['editor']
        print "Detail:",news_detail['new_body']



if __name__ == '__main__':
    sina = SinaNewsSpider('http://news.sina.com.cn/china/')
    sina.start()





