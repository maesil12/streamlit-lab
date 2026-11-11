# streamlit_app.py — 모든 페이지의 틀(진입 파일)
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Streamlit 실습", page_icon=":material/smart_toy:")

# API Key 입력칸은 사이드바에 두어 어느 페이지에서나 보이고 값이 유지되게 한다.
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", key="api_key")

# 다른 페이지에서도 쓸 수 있도록 OpenAI client를 session_state에 저장
if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)
else:
    st.session_state.pop("openai_client", None)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page("app_pages/Chatbot.py", title="Chatbot", icon=":material/local_library:"),
    st.Page("app_pages/ChatPDF.py", title="ChatPDF", icon=":material/picture_as_pdf:"),
])
pg.run()
