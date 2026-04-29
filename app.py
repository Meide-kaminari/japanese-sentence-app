import streamlit as st
import os
from openai import OpenAI

st.title("日语例句生成器")



def get_client():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        st.error("Missing API key")
        st.stop()

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

# 👉 不要在全局初始化 client
client = None

words_input = st.text_input("请输入多个单词（用空格隔开）")

if st.button("生成例句") and words_input:
    client = get_client()   # ✅ 在点击后再初始化

    words = words_input.split()

    for word in words:
        st.write(f"正在生成：{word}...")

        content = f"请用“{word}”写3个日语例句，并附中文翻译"

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": content}]
        )

        result = response.choices[0].message.content
        st.success(result)
