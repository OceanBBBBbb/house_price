# coding : UTF-8
import requests
import csv
import random
import time
import socket
import http.client
# import urllib.request
from bs4 import BeautifulSoup


# requests：用来抓取网页的html源代码
# csv：将数据写入到csv文件中
# random：取随机数
# time：时间相关操作
# socket和http.client 在这里只用于异常处理
# BeautifulSoup：用来代替正则式取源码中相应标签中的内容
# urllib.request：另一种抓取网页的html源代码的方法，但是没requests方便

def get_content(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'gb2312'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text


# 解析html
def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    data = body.find('div', {'id': 'newhouse_loupai_list'})  # 找到id为newhouse_loupai_list的div
    ul = data.find('ul')  # 获取ul部分
    li = ul.find_all('li')  # 获取所有的li

    list = []
    temp = ['名称','价格']
    list.append(temp)
    for day in li:  # 对每个li标签中的内容进行遍历
        try:
            temp = []
            name = day.find('div', {'class': 'nlcd_name'}).find('a').string.strip()  # 找到名称
            temp.append(name)  # 添加到temp中
            price = day.find('div', {'class': 'nhouse_price'}).find('span').get_text().strip()  # 找到价格
            temp.append(price)  # 第一个p标签中的内容（天气状况）加到temp中
            list.append(temp)
        except:
            print
            pass
        continue
    return list


# 生成表格
def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


# 主函数
if __name__ == '__main__':
    #http://cs.newhouse.fang.com/house/s/b92/?ctm=1.cs.xf_search.page.2
    #http://cs.newhouse.fang.com/house/s/b95/?ctm=1.cs.xf_search.page.6
    #http://cs.newhouse.fang.com/house/s/b94/?ctm=1.cs.xf_search.page.5
    city_simple = 'sh'  #城市简称，长沙cs，北京bj(北京的url特殊一点，不需要第一个bj.)
    for i in range(20):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, city_simple+'_houseprice.csv')
    print("获取结束")
