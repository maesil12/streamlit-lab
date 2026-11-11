# Streamlit 실습 (113731 생성AI응용프로그래밍)

- `streamlit_app.py` : 진입 파일 (사이드바 API Key 입력 + 페이지 이동)
- `app_pages/Home.py` : 실습 3·4 — 질문 응답(`gpt-6-luna`) + 이미지 생성(`gpt-image-2.6-flare`)
- `app_pages/Chat.py` : 실습 5 — 대화 기억 챗봇 (스트리밍, Clear 버튼)
- `app_pages/Chatbot.py` : 실습 6 — 국립부경대학교 도서관 규정 챗봇
- `app_pages/ChatPDF.py` : 실습 7 — PDF 업로드 후 File Search로 대화

OpenAI API Key는 코드나 저장소에 저장하지 않고, 웹 페이지 사이드바에서 입력받습니다.

```bash
pip install streamlit openai
streamlit run streamlit_app.py
```
