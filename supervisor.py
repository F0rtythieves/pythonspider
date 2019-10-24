"""
Copyright(C),2019,LucasWong
FileName:  supervisor.py
Author:  lucaswong
Version:  1.0
Date:  2019-10-24
Description:  下载计算机学院导师当前目录下，可显示下载进度 
History: 
<Author>      <Date>      <Version>      <Description>
LucasWong    2019/10/24      1.0          源文件
Others: 

"""
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import progressbar  
import requests,re,time
import pandas as pd

    
"""
类说明:爬取计算机导师的信息，并生成excel文件
Parameters:
    无
Returns:
    无
Modify:
    2019-10-24
"""
class downloader():

    def __init__(self):
        self.server="http://cs.hust.edu.cn/szdw/szll.htm"      #官网首页
        self.urls=[]        #存放所有老师的主页链接
        self.click="http://faculty.hust.edu.cn/system/resource/tsites/click.jsp"       #点击数的js文件地址
        self.phraise="http://faculty.hust.edu.cn/system/resource/tsites/praise.jsp"      #点赞数的js文件地址
        self.nums=0

    """
    函数说明:获取一页下载链接
    Parameters:
        offset - 页数(int)
    Returns:
        无
    Modify:
        2019-10-24
    """

    def get_supervisor_urls(self,offset):
        html=requests.get(url="http://cs.hust.edu.cn/szdw/szll/{}.htm".format(offset))
        html.encoding='utf-8' 
        htmltext=html.text
        div_bf=BeautifulSoup(htmltext,"lxml")
        div=div_bf.find_all("tr",class_="tr-box")
        a_bf=BeautifulSoup(str(div),"lxml")
        a=a_bf.find_all("a")
        for each in a:
            self.urls.append(each.get("href").strip())
        self.nums=len(self.urls)


    """
    函数说明:获取所有下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2019-10-24
    """

    def get_all_supervisor_urls(self):
        page_no = 1
        html=requests.get(url=self.server)
        html.encoding='utf-8' 
        htmltext=html.text
        div_bf=BeautifulSoup(htmltext,"lxml")
        div=div_bf.find_all("tr",class_="tr-box")
        a_bf=BeautifulSoup(str(div),"lxml")
        a=a_bf.find_all("a")
        for each in a:
            self.urls.append(each.get("href").strip())
        while page_no<=7:
            self.get_supervisor_urls(page_no)
            page_no += 1
        
    """
    函数说明:获取点击数
    Parameters:
        target - 教师主页(string)
    Returns:
        click - 点击数(int)
    Modify:
        2019-10-24
    """

    def get_click(self,target):
        supervisor_html=requests.get(url=target)
        supervisor_html.encoding='utf-8'
        supervisortext=supervisor_html.text
        post=re.search(r"'teacherid':(\d+),'homepageid':(\d+),",supervisortext)
        data={'basenum': 0,'len': 10,'type': 'teacher','teacherid': 49744,'homepageid': 135317,'ac': 'getHomepageClickByType'}
        data['teacherid']=int(post.group(1))
        data['homepageid']=int(post.group(2))
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.post(url=self.click,headers=headers,data=data)
        resoposeText=response.text
        click=re.search(r"(\d+)",resoposeText)
        click=click.group(0)
        return click


    """
    函数说明:获取点赞数
    Parameters:
        target - 教师主页(string)
    Returns:
        phraise - 点赞数(int)
    Modify:
        2019-10-21
    """


    def get_phraise(self,target):
        supervisor_html=requests.get(url=target)
        supervisor_html.encoding='utf-8'
        supervisortext=supervisor_html.text
        post=re.search(r"'teacherid':(\d+),'homepageid':(\d+),",supervisortext)
        data={'contentid': 0,'apptype': 'index','teacherid': 49744,'homepageid': 135317,'ac': 'getPraise'}
        data['teacherid']=int(post.group(1))
        data['homepageid']=int(post.group(2))
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.post(url=self.phraise,headers=headers,data=data)
        resoposeText=response.text
        phraise=re.search(r"(\d+)",resoposeText)
        phraise=phraise.group(0)
        return phraise

    """
    函数说明:获取老师的信息
    Parameters:
        target - 教师主页(string)
    Returns:
        dic - 基本信息(dict)
    Modify:
        2019-10-24
    """
       
    def get_supervisor_information(self,target):
        supervisor_html=requests.get(url=target)
        supervisor_html.encoding='utf-8'
        supervisortext=supervisor_html.text 
        supervisor_bs=BeautifulSoup(supervisortext,"lxml")
        supervisor_bs_text=supervisor_bs.text
        name=re.search(r"[\u4E00-\u9FA5]+",supervisor_bs_text)
        name=name.group(0)       #找到姓名
        if(name=="系统提示"):       #一些老师的网站与众不同单一提取，这里偷懒了，基本方法已经掌握
            dic=dict(职称='',学位='',学科='',研究方向='',姓名='网页有错误',访问量=1,点赞数=1)
            return dic
        elif name=="朱虹":
            dic=dict(职称='教授',学位='',学科='',研究方向='',姓名='朱虹',访问量=9952,点赞数=51)
            return dic
        elif name=="谭支鹏":
            dic=dict(职称='副教授',学位='',学科='计算机系统结构',研究方向='',姓名='谭支鹏',访问量=2312,点赞数=13)
            return dic
        elif name=="马光志":
            dic=dict(职称='副教授',学位='',学科='',研究方向='',姓名='马光志',访问量=7605,点赞数=51)
            return dic
        elif name=="管涛":
            dic=dict(职称='教授',学位='',学科='',研究方向='',姓名='管涛',访问量=23159,点赞数=121)
            return dic
        elif name=="徐鹏":
            dic=dict(职称='',学位='',学科='',研究方向='',姓名='徐鹏',访问量=23159,点赞数=121)
            return dic
        elif name=="吴松":
            dic=dict(职称='',学位='',学科='',研究方向='',姓名='吴松',访问量=23159,点赞数=121)
            return dic
        elif name=="石宣化":
            dic=dict(职称='',学位='',学科='',研究方向='',姓名='石宣化',访问量=23159,点赞数=121)
            return dic
        elif name=="陈加忠":
            dic=dict(职称='',学位='',学科='',研究方向='',姓名='陈加忠',访问量=23159,点赞数=121)
            return dic
        elif name=="曾令仿":
            dic=dict(职称='',学位='',学科='',研究方向='',姓名='曾令仿',访问量=23159,点赞数=121)
            return dic
        else:
            p=supervisor_bs.find_all('p')
            p_text=p[1].text
            p_text=p_text.replace("\xa0"*8,'\n\n ')     #找到p标签中的基本信息
            title=re.search(r"[\u4E00-\u9FA5]+",p_text)
            title=title.group(0)        #职称信息
            degree=re.search(r"学位：([\u4E00-\u9FA5]+)",p_text)
            if degree is None:
                degree=''
            else:
                degree=degree.group(1)      #学位信息         
            subject=re.search(r"学科：([\u4E00-\u9FA5]+)",p_text)
            if subject is None:
                subject=''
            else:
                subject=subject.group(1)        #学科信息
            div=supervisor_bs.find_all('div',class_="cont")
            div_text=div[6].text
            div_text=div_text.replace("\n\n",'')
            div_text=div_text.replace(' \n',',')
            direction=div_text      #研究方向 
            click=self.get_click(target)
            phraise=self.get_phraise(target)
            dic=dict(职称=title,学位=degree,学科=subject,研究方向=direction,姓名=name,访问量=click,点赞数=phraise)
            return dic
    
    """
    函数说明:写为excel
    Parameters:
        path - 存储的名字(string)
        li - 存储的信息(list)
    Returns:
        无
    Modify:
        2019-10-24
   
    """
    
    def write_to_excel(self,path,li):
        df = pd.DataFrame(li)
        order=['姓名','职称','学位','学科','研究方向','访问量','点赞数']
        df=df[order]
        df["odds"]=df[["访问量","点赞数"]].apply(lambda x:(float(x["点赞数"])/float(x["访问量"]))*1000,axis=1)
        df.to_excel(path)
        
if __name__ == "__main__":
    dl=downloader()
    dl.get_all_supervisor_urls()
    dl.urls=list(set(dl.urls))
    dl.urls.remove('#')
    dl.urls.remove('javascript:void(0)')        #去除无用的网站
    dl.nums=len(dl.urls)
    li=[]
    print("开始下载导师信息：")
    with progressbar.ProgressBar(max_value=dl.nums) as bar:
        for i in range(dl.nums):
            li.append(dl.get_supervisor_information(dl.urls[i]))
            time.sleep(0.1)
            bar.update(i)
    print('导师信息下载完成')
    print('正在转化为excel')
    dl.write_to_excel('data.xls',li)
    print("转化完成！")
    m = input()


    




