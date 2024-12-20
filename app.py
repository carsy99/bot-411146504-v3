# -*- coding: utf-8 -*-

# 載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import re

app = Flask(__name__)

# 必須放上自己的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('dBMC7H/SUd34Lkpn9oZ6qocYQ0clxHAz2kZ8NH+wbHOTwk6AwHZ82GyHmP2CElqTskoBrysRTapSBH5H/vwJkGaxpNUs5+wRs3ZY55SumhitebTEAdUvoLVKPaV74GwRCNVFtdZBRRQz8LPQg+yE0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6d7fa87c5ab818f1b4932b961b505758')

# 啟動訊息
line_bot_api.push_message('Uff01574d2181c7d50c1021ce1eaad953', TextSendMessage(text='LINE Bot 已啟動！'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text

    if re.match('推薦景點', message):
        carousel_template_message = TemplateSendMessage(
            alt_text='旅遊景點推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kNBl363.jpg',
                        title='台灣',
                        text='探索台灣的美麗風景',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='台灣熱門景點包括台北101、逢甲夜市、墾丁等。'
                            ),
                            URIAction(
                                label='了解更多',
                                uri='https://en.wikipedia.org/wiki/Taiwan'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/GBPcUEP.png',
                        title='日本',
                        text='體驗日本的文化與風景',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='日本熱門景點包括金閣寺、淺草寺、北海道等。'
                            ),
                            URIAction(
                                label='了解更多',
                                uri='https://en.wikipedia.org/wiki/Japan'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kRW5zTO.png',
                        title='韓國',
                        text='感受韓國的魅力文化',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='韓國熱門景點包括釜山、濟州島、首爾塔等。'
                            ),
                            URIAction(
                                label='了解更多',
                                uri='https://en.wikipedia.org/wiki/Korea'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入 "推薦景點" 來獲得旅遊資訊推薦！'))

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
