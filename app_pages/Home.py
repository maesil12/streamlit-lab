# 실습 3, 4 — 질문 응답 + 이미지 생성
import base64

import streamlit as st

TEXT_MODEL = "gpt-6-luna"
IMAGE_MODEL = "gpt-image-2.6-flare"

st.title("Home")

client = st.session_state.get("openai_client")
if client is None:
    st.info("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")


# 실습 3: 입력이 변하지 않으면 재실행 시 저장된 결과를 반환
# (client는 해시할 수 없으므로 매개변수 이름 앞에 _를 붙여 캐시 키에서 제외)
@st.cache_data(show_spinner=False)
def get_answer(_client, question):
    response = _client.responses.create(
        model=TEXT_MODEL,
        input=question,
    )
    return response.output_text


st.header("질문하기")
question = st.text_input("질문을 입력하세요")

if question and client:
    with st.spinner("답변 생성 중..."):
        try:
            answer = get_answer(client, question)
            st.write(answer)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

st.divider()

# 실습 4: 프롬프트 입력 후 버튼을 누르면 이미지 생성
st.header("이미지 생성")
prompt = st.text_input("이미지 프롬프트를 입력하세요")

if st.button("이미지 생성", disabled=client is None):
    if not prompt:
        st.warning("프롬프트를 먼저 입력하세요.")
    else:
        with st.spinner("이미지 생성 중... (수십 초 걸릴 수 있어요)"):
            try:
                img = client.images.generate(
                    model=IMAGE_MODEL,
                    prompt=prompt,
                )
                image_bytes = base64.b64decode(img.data[0].b64_json)
                # 다른 입력으로 페이지가 다시 실행돼도 이미지가 남도록 저장
                st.session_state["home_image"] = image_bytes
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 메모리 상의 이미지 보여주기
if "home_image" in st.session_state:
    st.image(st.session_state["home_image"])
