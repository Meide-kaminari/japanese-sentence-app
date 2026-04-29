import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载.env
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


st.title("日语例句生成器")

# 输入多个单词
words_input = st.text_input("请输入多个单词（用空格隔开）：")

if st.button("生成例句") and words_input:
    words = words_input.split()

    # 读取已有内容
    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = ""

    for word in words:
        if f"单词：{word}" in existing_content:
            st.warning(f"{word} 已存在，显示已有例句")

            # 从文件中提取该单词的内容（简单版本）
            parts = existing_content.split("=" * 20)
            for part in parts:
                if f"单词：{word}" in part:
                    st.write(part)
                    break

            continue

        st.write(f"正在生成：{word}...")

        content = f"""
请用“{word}”写3个日语例句，并附中文翻译
"""

        with st.spinner("AI生成中..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": content}
                ]
            )

        result = response.choices[0].message.content

        # 显示在网页
        st.success(f"{word} 生成完成")
        st.write(result)

        # 写入文件
        with open("result.txt", "a", encoding="utf-8") as f:
            f.write("=" * 20 + "\n")
            f.write(f"单词：{word}\n")
            f.write("新例句：\n")
            f.write(result + "\n\n")