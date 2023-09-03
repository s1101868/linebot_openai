import openai

# 设置OpenAI API的密钥
openai.api_key = "OPENAI_API_KEY"

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
