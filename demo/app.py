# demo/app.py

import streamlit as st

from demo.user_data import UserData
from demo.gallery import gallery, single_symbol
from demo.functions import process_sentence


st.session_state.user_data: UserData = UserData()
st.session_state.user_data.download_userdata()

st.set_page_config(page_title="AAC Symbol Generator", page_icon=":art:")

st.title("GenAAC Demo")
st.space("medium")

sentence = st.text_input("AAC Symbol로 생성할 문장이다 단어를 입력해주세요.")
button = st.button("AAC Symbol 생성")

if sentence:
    with st.spinner("AAC Symbol 생성 중..."):
        pairs = process_sentence(sentence, st.session_state.user_data)
        st.session_state.current_pairs = pairs

if st.session_state.get("current_pairs", False):
    cols = st.columns(len(st.session_state.current_pairs))
    for col, pair in zip(cols, st.session_state.current_pairs):
        with col:
            single_symbol(pair, st.session_state.user_data, key_prefix="current", size_factor=1.5)


if button and not sentence:
    st.error("문장을 입력해주세요.")

st.space("medium")
st.divider()
st.space("medium")

gallery(st.session_state.user_data)



st.write(f"user_id: {st.session_state.user_data.user_id}")