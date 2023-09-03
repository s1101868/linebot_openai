from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import os

# 导入你的 QA 模型函数
from qa_model import qa_function

app = Flask(__name__)

# Channel Access Token 和 Channel Secret，确保你的环境变量中有这些值
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 处理 LINE Bot 的 Webhook 请求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 处理用户发送的消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    # 使用 QA 模型获取回答
    qa_answer = qa_function(msg)

    # 发送 QA 模型的回答给用户
    line_bot_api.reply_message(event.reply_token, TextSendMessage(qa_answer))

if __name__ == "__main__":
    # 获取端口号，如果没有设置，默认使用 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


