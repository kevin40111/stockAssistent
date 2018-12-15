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

def reply(request):

    messages = transport['火車']['info']()

    result = []
    count = 0
    for message in messages:
        if count >= 5: break
        result.append( TextSendMessage(text=textMessageTemplate(message)) )
        count += 1

    return result

transport = {
        '火車': {
            'website': 'https://www.railway.gov.tw/tw/news.aspx?n=21560',
            'info': trainInfo
        },
        '公車': {
            'website': ''
        },
        '高鐵': {
            'website': ''
        },
        '捷運': {
            'website': ''
        },
}
