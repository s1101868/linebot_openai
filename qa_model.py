import csv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# 設定 OpenAI API 金鑰
import os
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')  # 請更換為您的 API 金鑰

class Document:
    def __init__(self, content, metadata=None):
        self.page_content = content
        self.metadata = metadata or {}

class CSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [Document(row[0]) for row in reader]

# 指定檔案路徑
file_path = "test.csv"  # 請更換為您的 CSV 文件路徑

# 建立加載器並加載文本
loader = CSVLoader(file_path)
texts = loader.load()

# 嵌入和向量存儲
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# 建立對話鏈
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.2), vectorstore.as_retriever())

chat_history = []

# 處理 LINE Bot 的消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 使用 QA 模型获取回答
    qa_answer = qa_function(user_message)  # 请确保定义了 qa_function

    # 发送 QA 模型的回答给用户
    line_bot_api.reply_message(event.reply_token, TextSendMessage(qa_answer))


