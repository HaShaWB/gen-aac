# demo/app.py

from typing import Literal

import streamlit as st

from widgets import login, sentence_widget, gallery_view


st.set_page_config(
    page_title="GenAAC",
    layout="wide",
)


if "user_id" not in st.session_state:
    login()

else:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "sentence"
    
    with st.sidebar:
        st.title("GenAAC")
        
        page = st.radio(
            "페이지 선택",
            ["sentence", "gallery"],
            format_func=lambda x: "문장 변환" if x == "sentence" else "갤러리",
            key="current_page"
        )
    
    _, center, _ = st.columns([1, 3, 1])

    with center:
        if st.session_state.current_page == "sentence":
            sentence_widget()
        else:
            gallery_view()
