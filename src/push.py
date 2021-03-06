from linebot.models import TextSendMessage
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi
)
import os
import requests
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler

last_post_time = datetime.now()

def pushMessage():
    global last_post_time
    resp = requests.get(
        'https://scweb.cwb.gov.tw/EarthquakeAdv.aspx',
        params={'ItemId': '57', 'loc': 'tw'},
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    )

    resp.encoding = 'UTF-8'
    html_doc = resp.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    quakes = soup.select_one('table.datalist2')
    newestquake = quakes.select('tr')[1]

    quaketime = newestquake.select('td')[1].select_one('a').string
    times = quaketime.split(' ')[1].split(':')
    dates = quaketime.split(' ')[0].split('/')

    realQuaketime = datetime(int(dates[0]), int(dates[1]), int(dates[2]), int(times[0]), int(times[1]))

    print(last_post_time)
    message = False
    if(realQuaketime > last_post_time):
        last_post_time = realQuaketime
        try:
            message = TextSendMessage(
                text='地震消息：' +
                newestquake.select('td')[4].select_one('a').string
                + ' 在 ' + newestquake.select('td')[1].select_one('a').string
                + ' 發生了規模 ' +
                newestquake.select('td')[2].select_one('a').string
                + ' 深度 ' + newestquake.select('td')[3].select_one('a').string
                + ' 的地震!!!'
            )
        except:
            message = False

    return message

def pushList():
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
        conn.close()
    except Exception:
        print(Exception)

    return rows

def process():
    api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
    message = pushMessage()
    if(message):
        for to in pushList():
            api.push_message(to[0], message)

def start():
    sched = BackgroundScheduler()
    sched.add_job(process, 'interval', seconds=60)
    sched.start()
