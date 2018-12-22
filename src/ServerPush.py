from linebot.models import TextSendMessage
from linebot import LineBotApi
from datetime import datetime
from bs4 import BeautifulSoup

import os
import requests

import psycopg2

if os.environ.get('ENVIRONMENT') == 'development':
    line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'), 'http://localhost:8080')
else:
    line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))

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
    quaketimestamp = datetime.strptime(quaketime, '%Y/%m/%d %H:%M').timestamp()*1000
    minute = datetime.now().minute
    if(minute == 59):
        minute = 0
    else:
        minute -=1

    if(quaketimestamp < datetime.now().replace(minute= minute, second=0, microsecond=0).timestamp()*1000):
        return
    
    message = TextSendMessage(
        text='地震消息：/n' + newestquake.select('td')[4].string 
            + ' 在 ' + newestquake.select('td')[1].string
            + ' 發生了規模 ' + newestquake.select('td')[2].string
            + ' 深度 ' + newestquake.select('td')[3].string
            + ' 的地震!!!'
    )
    pushMessage(message)

def pushMessage(message):
    try:
        conn = psycopg2.connect(
            dbname="group5pg", user="postgres", host="hci.dianalab.net", password="c8eccf33282708be620bb689dd54c2e8", port="10715"
        )
        print("I am connect to the database")
    except:
        print("I am unable to connect to the database")

    rows = []
    try:
        cur = conn.cursor()
        query = "select * from users;"
        cur.execute(query)
        conn.commit()
        rows = cur.fetchall()

    except Exception:
        print(Exception)

    for to in rows:
        line_bot_api.push_message(to[0], message)
