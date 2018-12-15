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
        print(value)
        if key == 'text':
            txt += value
        if key == 'link':
            txt += str(a(value, href=value))
        txt += '<br>'

    return txt + '<br>'


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


def transportation(request):
    parameter = request.split(',')


def reply(request):

    messages = transport['火車']['info']()

    result = ''
    for message in messages:
        result += textMessageTemplate(message)

    return TextSendMessage(text=result)

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
