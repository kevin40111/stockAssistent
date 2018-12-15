from flask import Flask, request, abort
import os
import sys
sys.path.append('./src')

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
    map = {
        '災害': 'disaster',
        '預防': 'prevention',
        '檢測': 'detection',
        '交通': 'traffic',
        '歷史資料': 'history',
    }

    try:
        spelate = ':' if event.message.text.find(':') != -1 else '：'
        split = event.message.text.split(spelate)
        module = __import__(map[split[0]])

        #回傳一個message的物件集合 size between 1 and 5
        messageOBJ_array = module.reply(split[1])

    except:
        messageOBJ_array = TextSendMessage(text='請輸入符合的參數結構 ex 交通:火車')

    line_bot_api.reply_message(
        event.reply_token,
        messageOBJ_array
    )

if __name__ == "__main__":
    app.run()
