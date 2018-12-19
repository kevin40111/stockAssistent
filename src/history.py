
from dominate import document
from dominate.tags import *
from dominate.util import raw
from bs4 import BeautifulSoup
import requests

from linebot.models import (
    TextSendMessage, ImageSendMessage, ImagemapSendMessage, URIImagemapAction, ImagemapArea, MessageImagemapAction, BaseSize
)

def search_news(request):
    method = request.split(':')[0]
    parameter = request.split(',')
    website = 'http://news.ltn.com.tw'
    resp = requests.get(
        website + '/search',
        params={
            'keyword': parameter[0],
            'page': parameter[1] if len(parameter) > 1 else 1
        },
    )
    resp.encoding = 'UTF-8'
    html_doc = resp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    news = soup.select_one('#newslistul').select('li')

    message = ''
    for n in news:
       txt = n.select_one('.tit').select_one('p').string
       if txt:
            message += 'title:' + txt + '<br>'
            message += 'tag:' + n.select_one('.immtag').string + '<br>'
            url = website + '/' + n.select_one('a.tit').get('href')
            message += 'link:' + str(a(url, href=url)) + '<br>'
            message += '<br><br>'
    return message

def reply(request):
    return ImagemapSendMessage(
        base_url='https://example.com/base',
        alt_text='this is an imagemap',
        base_size=BaseSize(height=1040, width=1040),
        actions=[
            URIImagemapAction(
                link_uri='https://example.com/',
                area=ImagemapArea(
                    x=0, y=0, width=520, height=1040
                )
            ),
            MessageImagemapAction(
                text='hello',
                area=ImagemapArea(
                    x=520, y=0, width=520, height=1040
                )
            )
        ]
    )
