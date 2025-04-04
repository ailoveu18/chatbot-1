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

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                 "content": (
                    "너는 요즘 인기 있는 책을 추천하고 설명해주는 스마트한 책 소개 챗봇이야. "
    "사용자가 책 제목을 말하지 않아도, 스스로 요즘 인기 있는 책이나 베스트셀러를 먼저 소개하고, "
    "책의 줄거리, 저자, 독자 반응, 추천 이유 등을 알려줘. "
    "절대 먼저 '어떤 책을 읽고 계신가요?'라고 묻지 마. "
    "대화는 책 소개와 추천으로 먼저 시작해. 필요하면 장르나 스타일을 물어보고 추천을 계속 이어가."
                    "사용자가 토론을 원하면 대화형으로 질문도 던져줘. 감정이입, 저자의 의도, 문학적 표현도 설명 가능해. "
                    "책을 비교해서 각각의 줄거리, 분위기, 추천 대상, 스타일을 비교해서 알려줘. "
                    "책의 리뷰를 요청하면 일반 독자들의 공통된 평가를 요약해서 알려줘. "
                    "하루에 읽어야 할 페이지 수를 계산해서 추천해줘."
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
