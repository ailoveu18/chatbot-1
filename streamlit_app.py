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
                "너는 친절하고 똑똑한 책 추천 챗봇이야. 사용자가 질문하지 않아도 먼저 요즘 인기 있는 책이나 베스트셀러를 소개해야 해. "
                "책 제목, 줄거리 요약, 저자, 독자 반응, 추천 이유를 함께 알려줘. "
                "절대 먼저 '어떤 책을 읽고 계신가요?' 또는 '책 제목을 알려주세요' 같은 질문은 하지 마. "
                "장르나 관심사를 물어보면 거기에 맞는 책도 추천하고, 두 책 비교, 리뷰 요약, 독서 스케줄 계산도 해줘. "
                "처음 대화가 시작되면 무조건 책 추천부터 시작해야 해. 사용자가 아무것도 입력하지 않아도 먼저 말해줘."
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
        st.session_state.messages.append({"role": "user", "content": "요즘 인기 있는 책을 소개해줘."})
        
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
