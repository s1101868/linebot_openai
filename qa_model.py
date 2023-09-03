import csv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from linebot.models import TextSendMessage
# 設定 OpenAI API 金鑰
import os
os.environ["OPENAI_API_KEY"] =" "  # 請更換為您的 API 金鑰

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

def send_message(query=None):

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
    while True:
        if query == None:
            break
        result = qa({"question": query + '(用繁體中文回答)', "chat_history": chat_history})
        print('A:', result['answer'])
        chat_history.append((query, result['answer']))
    return TextSendMessage(result)
   

