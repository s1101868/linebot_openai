from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

#======這裡是呼叫的檔案內容=====
from qa_model import *
#======這裡是呼叫的檔案內容=====

# 设置OpenAI API的密钥
openai.api_key = os.getenv('OPENAI_API_KEY')

# 初始化Line Bot
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 定义QA函数
def qa_function(user_input):
    # 使用GPT-3模型来生成回答
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        temperature=0.7,
        max_tokens=50
    )

    # 提取生成的回答文本
    answer = response.choices[0].text.strip()

    return answer

# 处理Line Bot的Webhook请求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 处理用户消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 使用QA模型获取回答
    qa_answer = send_message(user_message)

    # 发送回答给用户
    line_bot_api.reply_message(event.reply_token,qa_answer)

# 启动Flask应用
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



