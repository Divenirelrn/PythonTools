#-*- coding: utf-8 -*-
#time: 2020-11-10
#author: xiaojun
import urllib.request
from urllib.parse import urlencode
import re
import requests
import os
import sys
import time
from bs4 import BeautifulSoup
#导入目录处理方法

def get_urls(offset, topic):
    """
    urlopen请求网页
    :param offset: page num
    :return: urls
    """
    # url = 'https://image.baidu.com/search/index?'
    url = "https://image.baidu.com/search/flip?"
    params = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': topic,
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '0',
        'word': topic,
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'pn': offset * 30,
        'rn': '30',
        'gsm': '1e',
        '1537355234668': '',
    }
    url = url + urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    response = urllib.request.urlopen(req)
    if response.status != 200:
        return []
    html = response.read().decode('utf-8')
    r = re.compile("thumbURL.*?\.jpg")
    urls = r.findall(html)
    urls = [img_url.split(':', 1)[1][1:] for img_url in urls]
    return urls

# def get_urls(offset, topic):
#     """
#     requests请求网页
#     :param offset: page num
#     :return: urls
#     """
#     url = 'https://image.baidu.com/search/index?'
#     params = {
#         'tn': 'resultjson_com',
#         'ipn': 'rj',
#         'ct': '201326592',
#         'is': '',
#         'fp': 'result',
#         'queryWord': topic,
#         'cl': '2',
#         'lm': '-1',
#         'ie': 'utf-8',
#         'oe': 'utf-8',
#         'adpicid': '',
#         'st': '-1',
#         'z': '',
#         'ic': '0',
#         'word': topic,
#         's': '',
#         'se': '',
#         'tab': '',
#         'width': '',
#         'height': '',
#         'face': '0',
#         'istype': '2',
#         'qc': '',
#         'nc': '1',
#         'fr': '',
#         'expermode': '',
#         'pn': offset * 30,
#         'rn': '30',
#         'gsm': '1e',
#         '1537355234668': '',
#     }
#     url = url + urlencode(params)
#     print(url)
#     s = requests.Session()
#     s.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
#     response = s.get(url)
#     if response.status_code != 200:
#         return []
#     #beautifulsoup提取图像地址
#     # soup = BeautifulSoup(response.text, 'lxml')
#     # print(soup.find_all('script'))
#     #正则表达式提取图片地址
#     html = response.text
#     r = re.compile("thumbURL.*?\.jpg")
#     urls = r.findall(html)
#     urls = [img_url.split(':', 1)[1][1:] for img_url in urls]
#     return urls

def save_img(url, save_dir):
    """
    :param url: url of image
    :param save_dir: direcotory to save image
    :return: None
    """
    global count
    res = requests.get(url)
    if res.status_code == 200:
        save_path = os.path.join(save_dir, str(round(time.time() * 1000)) + '.jpg')
        with open(save_path, 'wb') as f:
            f.write(res.content)
        count += 1
        print('第%d张图片下载完成'%(count))


if __name__ == "__main__":
    # topics = ['甜甜圈', '杯子']
    file_name = r'D:\files\resources\Projects\object_detection\data\classes_add.txt'
    img_dir = r'D:\files\resources\Projects\object_detection\data\baidu_images'
    with open(file_name, 'r', encoding='utf-8') as fo:
        lines = fo.readlines()
    topics = [line.rstrip('\n').split(" ")[-1] for line in lines]
    page_num = sys.maxsize
    img_num = sys.maxsize
    save_dir = r"D:\files\resources\Projects\object_detection\data\baidu_images"
    for topic in topics:
        count = 0
        print('开始下载' + topic)
        topic_path = os.path.join(save_dir, topic)
        if not os.path.exists(topic_path):
            os.makedirs(topic_path)
        for i in range(page_num):
            time.sleep(0.5)
            urls = get_urls(i, topic)
            if len(urls) == 0:
                print('已到最后一页')
                break
            flag = 0
            for url in urls:
                save_img(url, topic_path)
                if count >= img_num:
                    flag = -1
                    break
            if flag == -1:
                break



