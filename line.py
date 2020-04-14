import psycopg2
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort
import sys
sys.path.append('./src')


app = Flask(__name__)

line_bot_api = LineBotApi(
    "Ioj/1iUb4Bh1rUUqoc0DXWyAsgarF0oOjHBiP/e/SxCJ+V3i5ZGdWpUWAcF6Mr/rACK9LTalK3MJfZkXy4omfnrsoUS9dKoyOJlQCV/q4nftBSQgZ0WViYgZqEBMw5s+fntZQvJLrhnwpNz4LpOo8QdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("b0532bf3b9affff65bbced87ba607b93")

__import__('push').start()


@app.route("/hellow", methods=['GET'])
def hellow():
    return 'Hellow World'


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
    # map = {
    #     '災害': 'disaster',
    #     '預防': 'prevention',
    #     '檢測': 'detection',
    #     '交通': 'traffic',
    #     '歷史資料': 'history',
    #     '使用者': 'users',
    #     '推播': 'broadcast'
    # }

    # try:
    #     conn = psycopg2.connect(
    #         dbname="group5pg", user="postgres", host="hci.dianalab.net", password="c8eccf33282708be620bb689dd54c2e8", port="10715"
    #     )
    #     cur = conn.cursor()
    #     query = "insert into users values ('{}');".format(event.source.user_id)
    #     cur.execute(query)
    #     conn.commit()
    #     conn.close()
    # except Exception:
    #     print(Exception)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    app.run()
