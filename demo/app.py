# demo/app.py

from typing import Literal

import streamlit as st

from widgets import login


st.set_page_config(
    page_title="GenAAC",
    layout="centered",
)


if "user_id" not in st.session_state:
    login()
