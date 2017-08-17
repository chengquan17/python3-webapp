#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import json
#import csv
#from urllib import parse
#from socket import timeout as socket_timeout
#from urllib import error
import time
#import random
import re
#from urllib.request import urlopen#
#from pprint import pprint
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import logging; logging.basicConfig(level=logging.INFO)


def getHtmlCode(url):  # 该方法传入url，返回url的html的源码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }
    # 增加异常处理，主要是会遇到requests.exceptions.ConnectionError异常
    #logging.debug('This is debug message')
    logging.info('处理地址：{}'.format(url))
    #logging.warning('This is warning message')
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        #print("Exception: {}".format(e))
        logging.error("Exception: {}".format(e))
        logging.info('延迟6分钟，保险起见！')
        # 延迟6分钟，保险起见！
        time.sleep(360)
        logging.info('处理地址：{}'.format(url))
        r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    #  台湾网页需要制定big5编码！！！
    #r.encoding = 'big5'
    page = r.text
    return page
    
def myGetTable(url, site, localPath):
    '''
    获取目录
    return:返回一个列表，每个值都是字典
    根据不同的网站需要修改这个函数
    '''
    ul = []
    #page = getHtmlCode(url)
    #bs_obj = BeautifulSoup(page, 'html.parser')
    i = 0 
    ul.append({'name': '0. MySQL 5.7 Reference Manual', 'url': url})
    while True: 
        logging.info('循环变量为：{}'.format(i)) 
        myGetContext(i + 1 , localPath, ul[i]['url'], ul[i]['name'])
        logging.info('已保存网页：{}'.format(ul[i]['name']))        
        tmpurl = myGetNext(ul[i]['url'], site)
        if not tmpurl:
            break
        tmpname = myGetName(tmpurl)
        tmpname = re.sub(r'\xa0', r' ', tmpname)
        #print('-'*10)
        logging.info('url:{}'.format(tmpurl))
        logging.info('name:{}'.format(tmpname))
        ul.append({'name': tmpname, 'url': tmpurl}) 
        i += 1     
        
    return ul
    
    
    

def myGetContext(num, localPath, url, name):
    """
    保存网页内容用于电子书制作
    :param num: 序号，用于路径
    :param localPath: 保存的路径
    :param name: 页面名称
    :param url: 网址
    :return:
    """    
    save_dir = Path(localPath)
    #print(name)
    # 考虑到name里面有各种不合规范的字符，不能用做文件名，故提取url的文件名
    #name = re.sub(r'\?', r'', name)
    #name = re.sub(r'\,', r'', name)
    filename2 = url.split('/')[-1]
    #print(name)
    
    filename1 = str(num) + '_' + filename2
    filename = save_dir / Path(filename1)
    logging.info('文件名:{}'.format(filename))
    # 判断文件是否存在，存在则跳过
    if filename.is_file():
        logging.info('文件已经存在！跳过！！！')
        return
    
    #print(filename)
    page = getHtmlCode(url)
    bs_obj = BeautifulSoup(page, 'html.parser')
    
    # 这里需要根据具体网站修改    
    for links in bs_obj.find_all('div', {'id': 'docs-body'}):
        #print(links)
        with open(filename, 'w', encoding='utf8') as f:
            f.write(str(links))

        
def myGetNext(url, site):
    """
    获取下一页的地址信息
    """    
    uln = []
    page = getHtmlCode(url)
    bs_obj = BeautifulSoup(page, 'html.parser')
    for links in bs_obj.find_all('a', {'title': re.compile("Next")}):
        uln.append({'name': links.get_text(), 'url': site + links['href']})
    #print("uln[0]['url']:",uln[0]['url'])
    if len(uln) > 0:
        return uln[0]['url']
    else:
        return None

def myGetName(url):
    """
    获取网页标题H1
    """    
    ul = []
    page = getHtmlCode(url)
    bs_obj = BeautifulSoup(page, 'html.parser')
    h1 = bs_obj.find_all(re.compile("h1|h2|h3|h4|h5|h6"), {'class': 'title'})
    #print(h1)
    return h1[0].get_text()   


if __name__ == '__main__':
    '''
    # auther: chengquan17
    # date: 2017年8月16日
    # mysql5.7在线文档，爬取了通过sigil制作epub电子书
    # requests 库 结合 beautifulSoup4 库的使用实例
    # 考虑到每一页都有Next按钮，利用这个功能逐页保存
    # 因为直接获取目录由于隐藏目录的存在不能成功！
    '''

    url = "https://dev.mysql.com/doc/refman/5.7/en/"
    site = "https://dev.mysql.com"
    site = url
        
    # localPath是自己设定的保存路径
    localPath = 'D:/dump/mysql_doc'
    path = Path(localPath)
    if not path.exists():
        path.mkdir()
    
    
    # ul保存目录链接
    page = getHtmlCode(url)
    #print(page)
    ul = []
    ul = myGetTable(url, site, localPath)
    #print(len(ul))
    logging.info('目录大小：{}'.format(len(ul)))
    #for link in ul:
    #    print(link)    


    #i = 0
    #for link in ul:
    #    #print(link)
    #    i = i + 1
    #    myGetContext(i, link['name'], link['url'])
    #
    #print("ul[0]['name']:",ul[0]['name'])
    #print("ul[0]['url']:",ul[0]['url'])
    #print("ul[1]['name']:",ul[1]['name'])
    #print("ul[1]['url']:",ul[1]['url'])
    #print("ul[2]['name']:",ul[2]['name'])
    #print("ul[2]['url']:",ul[2]['url'])
    myGetContext(1, localPath, ul[1]['url'], ul[1]['name'])
    
    
    #for links in bs_obj.find_all('div', {'class': 'x-content'}):
    #    print(links)







