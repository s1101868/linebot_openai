import csv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from linebot import WebhookHandler, LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

#======這裡是呼叫的檔案內容=====
from qa_function import *
#======這裡是呼叫的檔案內容=====


# 設定 OpenAI API 金鑰
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')  # 請更換為您的 API 金鑰

# 初始化 LINE Bot
line_bot_api = LineBotApi("CHANNEL_ACCESS_TOKEN")
handler = WebhookHandler("CHANNEL_SECRET")

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
            return [Document(", ".join(row)) for row in reader]

def initialize_qa_system(file_path):
    # 指定檔案路徑
    # file_path = "test.csv"  # 請更換為您的 CSV 文件路徑
    file_path = os.path.join(os.getcwd(), "test.csv")  # 使用当前工作目录

    # 建立加載器並加載文本
    loader = CSVLoader(file_path)
    texts = loader.load()

    # 嵌入和向量存儲
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(texts, embeddings)

    # 建立對話鏈
    qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.2), vectorstore.as_retriever())

    return qa

if __name__ == "__main__":
    qa_system = initialize_qa_system("test.csv")
    chat_history = []  # 初始化聊天历史
   

