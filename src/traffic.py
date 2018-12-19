from dominate import document
from dominate.tags import *
from dominate.util import raw
from bs4 import BeautifulSoup
import requests
from linebot.models import (
    TextSendMessage
)

def textMessageTemplate(message):
    txt = ''
    for (key, value) in message.items():
        if key == 'text':
            txt += value
        if key == 'link':
            txt += value

    return txt


def mrtInfo():
    resp = requests.get(
        transport['捷運']['website'],
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    )

    resp.encoding = 'UTF-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    tags = soup.select('td.CCMS_jGridView_td_Class_1')
    message = []
    for tag in tags:
        try:
            message.append({
                'text': tag.select_one('span a')['title'],
                'link': 'https://www.metro.taipei/' + tag.select_one('span a')['href']
            })
        except:
            print('error')

    return message

def hightTranInfo():
    resp = requests.get(
        transport['高鐵']['website'],
        params={},
        headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    )
    tags = resp.json()

    message = []
    for tag in tags['NewsNewData']:
        try:
            message.append({
                'text': tag['Title'],
                'link': 'http://m.thsrc.com.tw/tw/News/Detail/' + tag['NewsId']
            })
        except:
            print('error')

    return message

def trainInfo():
    resp = requests.get(
        transport['火車']['website'],
        {},
    )
    resp.encoding = 'UTF-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    tags = soup.select('#DG tr')

    message = []
    for tag in tags:
        try:
            message.append({
                'text': tag.select_one('span')['title'],
                'link': 'https://www.railway.gov.tw/tw/' + tag.select_one('a')['href']
            })
        except:
            print('error')

    return message

transport = {
    '火車': {
        'website': 'https://www.railway.gov.tw/tw/news.aspx?n=21560',
        'info': trainInfo
    },
    '高鐵': {
        'website': 'http://m.thsrc.com.tw/tw/News/LoadMoreNews?skip=0&loadCount=5',
        'info': hightTranInfo
    },
    '捷運': {
        'website': 'https://www.metro.taipei/News.aspx?n=30CCEFD2A45592BF&sms=72544237BBE4C5F6',
        'info': mrtInfo
    },
}

def reply(request):
    messages = transport[request]['info']()
    result = []
    count = 0
    for message in messages:
        if count >= 5:
            break
        result.append(TextSendMessage(text=textMessageTemplate(message)))
        count += 1

    return result

reply('捷運')
