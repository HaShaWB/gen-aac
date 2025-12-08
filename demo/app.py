# demo/app.py

import streamlit as st

from demo.user_data import UserData
from demo.widgets import gallery, aac_from_keyword, aac_from_image
from genaac.config import CONFIG


st.session_state.user_data: UserData = UserData()
st.session_state.user_data.download_server()

st.set_page_config(page_title="AAC Symbol Generator", page_icon=":art:")

st.space("medium")
st.title("GenAAC Demo")

# 변환 모드 선택 (라디오 버튼)
mode = st.radio(
    "변환 모드 선택",
    ["단어 변환", "이미지 변환"],
    horizontal=True,
)

# 선택된 모드에 따라 위젯 렌더링
if mode == "단어 변환":
    aac_from_keyword()
else:
    aac_from_image()

st.space("medium")

gallery()
