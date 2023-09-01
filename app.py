pip install line-bot-sdk
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from qa_model import qa_function  # 导入你的 QA 模型函数的方式可能不同，根据实际情况修改导入语句


app = Flask(__name__)

# 用你的 Channel Secret 和 Channel Access Token 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

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
    GPT_answer = GPT_response(msg)  # 使用 GPT 模型获取初始回答

    # 使用 QA 模型获取更准确的回答
    qa_answer = qa_function(msg)

    # 输出 QA 模型的回答
    print(qa_answer)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(qa_answer))




if __name__ == "__main__":
    app.run()
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
