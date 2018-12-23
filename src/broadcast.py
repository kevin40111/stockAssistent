from linebot import (
    LineBotApi
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage
)
import psycopg2
import os

def reply(request):
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

    line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))

    for to in rows:
        line_bot_api.push_message(to[0], TextSendMessage(text=request))

    return TextSendMessage(text='推播成功')
