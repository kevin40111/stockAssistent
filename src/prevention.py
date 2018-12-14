from linebot.models import (
    TextSendMessage
)

def reply(request):
    return TextSendMessage(text=request)
