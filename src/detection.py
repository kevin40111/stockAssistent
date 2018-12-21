from linebot.models import (TextSendMessage)
from linebot.models import (TemplateSendMessage)
from linebot.models import actions, imagemap, template

import requests
from bs4 import BeautifulSoup

GasDIYList = [
    {'title':'瓦斯漏氣怎麼辦？「禁火、關氣、推窗、Call out」四步驟', 'url' : 'https://www.parenting.com.tw/article/5060567-%E7%93%A6%E6%96%AF%E6%BC%8F%E6%B0%A3%E6%80%8E%E9%BA%BC%E8%BE%A6%EF%BC%9F%E3%80%8C%E7%A6%81%E7%81%AB%E3%80%81%E9%97%9C%E6%B0%A3%E3%80%81%E6%8E%A8%E7%AA%97%E3%80%81Call+out%E3%80%8D%E5%9B%9B%E6%AD%A5%E9%A9%9F/'},
    {'title':'瓦斯漏氣 如何檢測保命', 'url' : 'http://news.ltn.com.tw/news/focus/paper/805362'}
]
WaterDIYList = [
    {'title':'地震造成水管內線破裂　台水提醒：用戶可自行檢查', 'url':'https://www.nownews.com/news/20160211/1993377/'},
    {'title':'「專訪」地震後該如何檢視居家結構安全無虞？特力幸福家', 'url':'http://decomyplace.com/newspost.php?id=4188'},
]
ElectricityDIYList = [
    {'title':'「地震停電」和颱風不一樣！　林金宏：復電恐引發大火', 'url':'https://www.ettoday.net/news/20160206/645060.htm'},
    {'title':'「專訪」地震後該如何檢視居家結構安全無虞？特力幸福家', 'url':'http://decomyplace.com/newspost.php?id=4188'},
]

def reply(request):
    funs = {
        '水電': lambda: createImagemap(),
        '大眾': lambda: createTemplateButtons(),
        '自來水新聞': lambda: createNews('自來水'),
        '電力新聞': lambda: createNews('電力'),
        '瓦斯新聞': lambda: createNews('瓦斯'),
        '居家': lambda: createHomeDetection(),
        '自來水': lambda: createDIYList('自來水'),
        '電力': lambda: createDIYList('電力'),
        '瓦斯': lambda: createDIYList('瓦斯'),
    }

    result = funs.get(request, lambda:TextSendMessage(text=request))()
    return result

def createImagemap():
    imagemap_message = imagemap.ImagemapSendMessage(
        base_url='https://i.imgur.com/piJcKim.png',
        alt_text='this is an imagemap',
        base_size=imagemap.BaseSize(height=391, width=500),
        actions=[
            imagemap.MessageImagemapAction(
                text='檢測:居家',
                area=imagemap.ImagemapArea(
                    x=0, y=91, width=250, height=391
                )
            ),
            imagemap.MessageImagemapAction(
                text='檢測:大眾',
                area=imagemap.ImagemapArea(
                    x=250, y=91, width=250, height=391
                )
            )
        ]
    )
    return imagemap_message

def createTemplateButtons():
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=template.ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/PEh153q.png',
            title='News!',
            text='Please select',
            actions=[
                actions.PostbackAction(
                    label='自來水新聞',
                    data='檢測:自來水新聞'
                ),
                actions.MessageAction(
                    label='電力新聞',
                    text='檢測:電力新聞'
                ),
                actions.MessageAction(
                    label='瓦斯新聞',
                    text='檢測:瓦斯新聞'
                )
            ]
        )
    )

    return buttons_template_message

def createNews(newsType):
    resp = requests.get(
        'https://www.google.com/search',
        params={ 'q': newsType, 'tbm': 'nws', 'start':'0'},
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    )
    resp.encoding = 'UTF-8'
    html_doc = resp.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    news = soup.select('.ts')

    ImgSoruce = {
        '自來水':   'https://i.imgur.com/KxbkZz6.png',
        '電力'  :   'https://i.imgur.com/YTuT4j6.jpg',
        '瓦斯'  :   'https://i.imgur.com/46bvScx.png'
    }[newsType]

    newsColums = []
    for n in news:
        col = template.CarouselColumn(
                thumbnail_image_url=ImgSoruce,
                title=''.join(list(n.select_one('.r').stripped_strings)),
                text=(''.join(list(n.select_one('.st').stripped_strings)))[:55] + '...',
                actions=[
                    actions.URIAction(
                        label='前往新聞頁面',
                        uri= n.select_one('.l')["href"]
                    )
                ]
            )
        newsColums.append(col)

    carousel_template_message = template.TemplateSendMessage(
        alt_text='Carousel template',
        template=template.CarouselTemplate(
            columns=newsColums
        )
    )
    return carousel_template_message

def createHomeDetection():
    buttons_template_message = template.TemplateSendMessage(
        alt_text='Buttons template',
        template=template.ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/dh9Oosl.png',
            # image_aspect_ratio='square',
            # image_size='contain',
            title='檢測DIY!',
            text='Please select',
            actions=[
                actions.PostbackAction(
                    label='自來水',
                    data='檢測:自來水'
                ),
                actions.MessageAction(
                    label='電力',
                    text='檢測:電力'
                ),
                actions.MessageAction(
                    label='瓦斯',
                    text='檢測:瓦斯'
                )
            ]
        )
    )
    return buttons_template_message

def createDIYList(DIYType):
    DIYList = {
        '自來水' : WaterDIYList,
        '電力'   : ElectricityDIYList,
        '瓦斯'   : GasDIYList
    }[DIYType]

    DIYColums = []
    for n in DIYList:
        col = template.CarouselColumn(
                # thumbnail_image_url=ImgSoruce,
                title=n['title'],
                text=DIYType,
                actions=[
                    actions.URIAction(
                        label='前往DIY頁面',
                        uri= n['url']
                    )
                ]
            )
        DIYColums.append(col)

    carousel_template_message = template.TemplateSendMessage(
        alt_text='Carousel template',
        template=template.CarouselTemplate(
            columns=DIYColums
        )
    )
    return carousel_template_message
