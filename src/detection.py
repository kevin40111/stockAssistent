from linebot.models import (TextSendMessage)
from linebot.models import actions, imagemap, template

import requests
from bs4 import BeautifulSoup

def reply(request):
    funs = {
        '水電': lambda: createImagemap(),
        '大眾': lambda: createTemplateButtons(),
        '自來水新聞': lambda: createNews('自來水'),
        '電力新聞': lambda: createNews('電力'),
        '瓦斯新聞': lambda: createNews('瓦斯')
    }
    result = funs.get(request, lambda:TextSendMessage(text=request))()
    return result

def createImagemap():
    imagemap_message = imagemap.ImagemapSendMessage(
        base_url='https://i.imgur.com/o7GBOxo.png',
        alt_text='this is an imagemap',
        base_size=imagemap.BaseSize(height=391, width=500),
        actions=[
            imagemap.URIImagemapAction(
                link_uri='https://example.com/',
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
    buttons_template_message = template.TemplateSendMessage(
        alt_text='Buttons template',
        template=template.ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/PEh153q.png',
            # image_aspect_ratio='square',
            # image_size='contain',
            title='News!',
            text='Please select',
            actions=[
                actions.PostbackAction(
                    label='自來水新聞',
                    text='檢測:自來水新聞'
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
        # print(''.join(list(n.select_one('.r').stripped_strings)))
        # try:
        #     print(n.select_one('.th')["src"])
        # except:
        #     print('nothing')
        col = template.CarouselColumn(
                thumbnail_image_url=ImgSoruce,
                title=''.join(list(n.select_one('.r').stripped_strings)),
                text=''.join(list(n.select_one('.st').stripped_strings)),
                actions=[
                    actions.PostbackAction(
                        label='postback1',
                        text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    actions.MessageAction(
                        label='message1',
                        text='message text1'
                    ),
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