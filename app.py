from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from qa_model import qa_function  # 导入你的 QA 模型函数的方式可能不同，根据实际情况修改导入语句

app = Flask(__name__)

# 假设你的环境变量已经正确设置
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # 获取请求的头部信息
    signature = request.headers['X-Line-Signature']
    # 获取请求的主体内容
    body = request.get_data(as_text=True)

    try:
        # 验证请求的签名是否正确，不正确则抛出异常
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    # 使用 QA 模型获取回答
    qa_answer = qa_function(msg)

    # 发送 QA 模型的回答给用户
    line_bot_api.reply_message(event.reply_token, TextSendMessage(qa_answer))

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

