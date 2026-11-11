# 실습 7 — ChatPDF: 업로드한 PDF 내용으로 대화 (OpenAI File Search)
import streamlit as st

MODEL = "gpt-6-luna"

st.title("ChatPDF")

client = st.session_state.get("openai_client")
if client is None:
    st.info("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


def clear_chat():
    """Clear: 대화 내용만 삭제"""
    st.session_state.pdf_messages = []


def leave():
    """Leave: vector store 삭제 후 다시 파일 업로드 화면으로"""
    vs_id = st.session_state.pop("pdf_vector_store_id", None)
    file_id = st.session_state.pop("pdf_file_id", None)
    st.session_state.pop("pdf_file_name", None)
    try:
        if vs_id:
            client.vector_stores.delete(vs_id)
        if file_id:
            client.files.delete(file_id)
    except Exception:
        pass  # 이미 삭제된 경우 등은 무시
    st.session_state.pdf_messages = []
    st.session_state.uploader_key += 1  # 업로더 초기화


# 1) 파일 업로드 화면: vector store가 아직 없을 때만 보여줌
if "pdf_vector_store_id" not in st.session_state:
    uploaded = st.file_uploader(
        "PDF 파일을 업로드하세요",
        type="pdf",
        accept_multiple_files=False,  # 파일은 하나만
        key=f"pdf_uploader_{st.session_state.uploader_key}",
    )
    if uploaded is None:
        st.stop()

    # 업로드한 파일로 vector store를 한 번만 만들고 session_state에 저장
    with st.spinner("PDF를 분석하는 중입니다..."):
        try:
            vector_store = client.vector_stores.create(name=uploaded.name)
            vs_file = client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=(uploaded.name, uploaded.getvalue(), "application/pdf"),
            )
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.stop()

    if vs_file.status != "completed":
        st.error(f"파일 처리에 실패했습니다: {vs_file.last_error}")
        client.vector_stores.delete(vector_store.id)
        st.stop()

    st.session_state.pdf_vector_store_id = vector_store.id
    st.session_state.pdf_file_id = vs_file.id
    st.session_state.pdf_file_name = uploaded.name
    st.session_state.pdf_messages = []
    st.rerun()

# 2) 대화 화면
st.success(f"📄 {st.session_state.pdf_file_name}")

col1, col2 = st.columns(2)
col1.button("Clear", on_click=clear_chat, use_container_width=True)
col2.button("Leave", on_click=leave, use_container_width=True)

for msg in st.session_state.pdf_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("PDF 내용에 대해 질문하세요"):
    st.session_state.pdf_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.responses.create(
                model=MODEL,
                instructions="업로드된 PDF 파일의 내용을 file_search로 찾아 그 내용을 바탕으로 답하라.",
                input=st.session_state.pdf_messages,
                tools=[{
                    "type": "file_search",
                    "vector_store_ids": [st.session_state.pdf_vector_store_id],
                }],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.pdf_messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
