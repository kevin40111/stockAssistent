from linebot.models import (
    TextSendMessage
)

import psycopg2

try:
    conn = psycopg2.connect(
        dbname="group5pg", user="postgres", host="hci.dianalab.net", password="c8eccf33282708be620bb689dd54c2e8", port="10715"
    )
    print("I am connect to the database")
except:
    print("I am unable to connect to the database")

def reply(request):
    rows = []
    try:
        cur = conn.cursor()
        query = "select * from users;"
        cur.execute(query)
        conn.commit()
        rows = cur.fetchall()

        for row in rows:
            print(row[0])

    except Exception:
        print(Exception)

    return TextSendMessage(text='print on hcidokkugroup5')