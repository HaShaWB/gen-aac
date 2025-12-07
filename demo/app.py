# demo/app.py

import streamlit as st

from demo.user_data import UserData
from demo.widgets.gallery import gallery


st.session_state.user_data: UserData = UserData()
st.session_state.user_data.download_server()

st.set_page_config(page_title="AAC Symbol Generator", page_icon=":art:")

st.space("medium")
st.title("GenAAC Demo")

chat = st.text_input("변환할 키워드를 입력해주세요.")

if chat:
    with st.spinner("Symbol 생성 중..."):
        pair = st.session_state.user_data.find_or_generate_symbol(chat)
        st.image(pair.image, width=320, output_format="PNG")
        st.header(pair.text)

st.space("medium")

gallery()
