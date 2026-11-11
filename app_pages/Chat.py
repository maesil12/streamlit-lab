# 실습 5 — 이전 대화를 기억하는 챗봇 (OpenAI Responses API, 스트리밍)
import streamlit as st

MODEL = "gpt-6-luna"

st.title("Chat")

# 대화 내용을 session_state에 저장해 이전 대화를 기억
if "messages" not in st.session_state:
    st.session_state.messages = []


def clear_chat():
    st.session_state.messages = []


st.button("Clear", on_click=clear_chat)

client = st.session_state.get("openai_client")
if client is None:
    st.info("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")

# 지금까지의 대화 보여주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요", disabled=client is None):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.responses.create(
                model=MODEL,
                input=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
