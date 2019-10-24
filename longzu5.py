"""
Copyright(C),2019,LucasWong
FileName:  longzu5.py
Author:  lucaswong
Version:  3.0
Date:  2019-10-21
Description:  下载多本网的小说龙族五到当前目录下，可显示下载进度 
History: 
<Author>      <Date>      <Version>      <Description>
LucasWong    2019/10/21      1.0          源文件
LucasWong    2019/10/21      2.0          去除广告信息
LucasWong    2019/10/21      3.0          添加进度条
Others: 

"""
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import progressbar  
import requests, sys,re,time

    
"""
类说明:下载多本网小说《龙族5》
Parameters:
    无
Returns:
    无
Modify:
    2019-10-21
"""
class downloader(object):
    
    def __init__(self):
        self.server="https://www.duoben.net"
        self.target="https://www.duoben.net/book/11893/"
        self.names=[]       #存放章节的名字
        self.urls=[]        #存放每个章节的链接
        self.nums=0         #章节数
    
    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2019-10-21
    """
    def get_download_url(self):
        req=requests.get(url=self.target)
        html=req.text
        div_bf=BeautifulSoup(html,"lxml")
        div=div_bf.find_all("div",class_="listmain")
        a_bf=BeautifulSoup(str(div[0]),"lxml")
        a=a_bf.find_all("a")
        self.nums=len(a)
        for each in a:
            self.names.append(each.string)
            self.urls.append(self.server+each.get("href"))

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2019-10-21
    """
    def get_contents(self,target):
        req=requests.get(url=target)
        html=req.text
        bf=BeautifulSoup(html,"lxml")
        texts=bf.find_all("div",class_="showtxt")
        texts=texts[0].text
        texts=re.sub('https(.*)net','',texts)
        texts=texts.replace("\xa0"*8,'\n\n ')
        return texts
    
    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2019-10-21
    """
    def writer(self,name,path,text):
        write_flag=True
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == "__main__":
    dl=downloader()
    dl.get_download_url()
    print("《龙族5》开始下载：")
    with progressbar.ProgressBar(max_value=dl.nums) as bar:
        for i in range(dl.nums):
            dl.writer(dl.names[i],'longzu5.txt',dl.get_contents(dl.urls[i]))
            time.sleep(0.1)
            bar.update(i)
    print('《龙族5》下载完成')
    m = input()


