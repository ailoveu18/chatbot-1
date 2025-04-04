import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📘 스마트 책 튜터")
st.write(
    "📘책📘책📘책📘쳇봇입니다! 책의 내용을 더 깊이 이해하고 싶을 때, 책 튜터와 함께 해보세요!"
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

      # 책 제목 및 요약 입력
    with st.expander("📖 책 정보 입력하기"):
        book_title = st.text_input("책 제목", placeholder="예: 데미안")
        book_summary = st.text_area("책 요약 또는 읽은 내용", placeholder="책 내용 요약이나 현재까지 읽은 부분을 적어주세요.")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 사용자의 독서를 도와주는 친절하고 지적인 책 튜터야.\n"
                    "사용자가 입력한 책 제목과 내용을 기반으로, 중요한 개념을 설명하거나, 등장인물의 행동을 분석하고, 어려운 문장을 쉽게 풀어서 설명해줘.\n"
                    "사용자가 토론을 원하면 대화형으로 질문도 던져줘. 감정이입, 저자의 의도, 문학적 표현도 설명 가능해."
                )
            }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input(""궁금한 점이나 토론하고 싶은 내용을 입력해보세요!"):

        # Store and display the current prompt.
        context_prompt = f"📘 책 제목: {book_title}\n📄 책 내용: {book_summary}\n\n🗨️ 질문: {prompt}"
        st.session_state.messages.append({"role": "user", "content": "너는 친절하고 똑똑한 책 튜터야. 사용자가 읽는 책 내용을 이해하도록 도와주는 역할을 해."})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
