import streamlit as st
import os
from openai import OpenAI

st.title("任崇雷的词典")

def get_client():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        st.error("Missing API key")
        st.stop()

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

client = None

words_input = st.text_input("请输入多个单词（用空格隔开）")

# ===== 彩蛋系统 =====
easter_eggs = {
    "任崇雷": "🤖 被你发现了制作者，没错，就是无敌帅气聪明的任崇雷",
    "王秀坤": "这个是制作者的朋友，不可以生成例句。",
    "张倍宁": "这个是大连第一美少女",
    "任官镇": "我爹",
}

if st.button("生成例句") and words_input:

    words = words_input.split()

    client = get_client()

    for word in words:

        # ===== 彩蛋逻辑 =====
        if word in easter_eggs:
            st.success(easter_eggs[word])
            continue   # ⚠️ 不要 stop，否则后面词会断掉

        st.write(f"正在生成：{word}...")

        content = f"请用“{word}”写3个日语例句，并附中文翻译"

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": content}]
        )

        result = response.choices[0].message.content
        st.success(result)
