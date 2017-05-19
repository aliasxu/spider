#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import re

#处理页面多余标签
class Tool:
    #去除img标签，7位长空格
    removeImg = re.compile('<img.*?>| {7}|&nbsp;')
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
    #将多行空行删除
    removeNoneLine = re.compile('\n+')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,'\n',x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,'\n',x)
        return x.strip()