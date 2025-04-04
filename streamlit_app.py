import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📘책📘책📘책📘쳇봇 ")
st.write(
    "📘책스케줄📘책비교📘책리뷰📘쳇봇입니다! 요즘 인기 있는 책이 궁금하신가요? 어떤 책을 읽어볼지 고민된다면, 저에게 물어보세요!"
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
                    "너는 요즘 인기 있는 책들을 소개해주는 친절한 독서 큐레이터 챗봇이야. "
                    "한국과 해외의 최신 베스트셀러들을 추천하고, 책 줄거리, 저자, 독자 후기, 추천 이유 등을 설명해줘. "
                    "사용자가 원하는 장르나 관심사를 말하면 그에 맞는 책도 추천해줘. "
                    "너는 사용자의 독서를 도와주는 친절하고 지적인 책 튜터야. "
                    "사용자가 입력한 책 제목과 내용을 기반으로, 중요한 개념을 설명하거나, 등장인물의 행동을 분석하고, 어려운 문장을 쉽게 풀어서 설명해줘. "
                    "사용자가 토론을 원하면 대화형으로 질문도 던져줘. 감정이입, 저자의 의도, 문학적 표현도 설명 가능해. "
                    "두 책을 비교해달라고 하면 각각의 줄거리, 분위기, 추천 대상, 스타일을 비교해서 알려줘. "
                    "특정 책의 리뷰를 요청하면 일반 독자들의 공통된 평가를 요약해서 알려줘. "
                    "사용자가 책을 며칠 안에 읽고 싶다고 하면 하루에 읽어야 할 페이지 수를 계산해서 추천해줘."
                )
            }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("궁금한 책이나 장르를 입력해보세요! 예: 요즘 베스트셀러는 뭐야?"):

        # Store and display the current prompt.
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
