from flask import Flask, request, abort
from dominate import document
from dominate.tags import *
from dominate.util import raw
import os

from bs4 import BeautifulSoup
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = None

if os.environ.get('ENVIRONMENT') == 'development':
    line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'), 'http://localhost:8080')
else:
    line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    message = search_news(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

def search_news(request):
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

    message =''
    for n in news:
       txt = n.select_one('.tit').select_one('p').string
       if txt:
            message += 'title:' + txt + '<br>'
            message += 'tag:' + n.select_one('.immtag').string + '<br>'
            url = website + '/' + n.select_one('a.tit').get('href')
            message += 'link:' + str(a(url, href=url)) + '<br>'
            message += '<br><br>'
    return message

if __name__ == "__main__":
    app.run()
