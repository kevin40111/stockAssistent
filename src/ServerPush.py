from linebot.models import TextSendMessage
from linebot import LineBotApi
from datetime import datetime
from bs4 import BeautifulSoup

import os
import requests

import psycopg2

def SearchQuakeList():
    resp = requests.get(
        'https://scweb.cwb.gov.tw/EarthquakeAdv.aspx',
        params={'ItemId':'57', 'loc':'tw'},
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    )

    resp.encoding = 'UTF-8'
    html_doc = resp.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    quakes = soup.select_one('table.datalist2')
    newestquake = quakes.select('tr')[1]

    quaketime = newestquake.select('td')[1].select_one('a').string
    print(quaketime)
    quaketimestamp = datetime.strptime(quaketime, '%Y/%m/%d %H:%M').timestamp()*1000
    now = datetime.now().minute
    if(now == 59):
        minute = 0
    else:
        now -= 1

    if(quaketimestamp < datetime.now().replace(hour= 8,minute= minute, second=0)):
        return False

    message = TextSendMessage(
        text='地震消息：/n' + newestquake.select('td')[4].string
            + ' 在 ' + newestquake.select('td')[1].string
            + ' 發生了規模 ' + newestquake.select('td')[2].string
            + ' 深度 ' + newestquake.select('td')[3].string
            + ' 的地震!!!'
    )
    return (message)


print(SearchQuakeList())
