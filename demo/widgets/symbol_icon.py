# demo/widgets/symbol_icon.py

import streamlit as st

from genaac.utils import ImageTextPair


def symbol_icon(keyword: str, pair: ImageTextPair):
    with st.container(
        border=True,
        width=160,
        height=240,
        horizontal_alignment="center",
        vertical_alignment="center",
    ):
        st.image(pair.image, width="stretch", output_format="PNG")
        st.button(
            label=f"### {keyword}",
            width="stretch",

        )