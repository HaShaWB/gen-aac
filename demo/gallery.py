# demo/gallery.py

import re

import streamlit as st

from genaac.utils import ImageTextPair
from demo.user_data import UserData
from demo.functions import process_keyword, process_image_keyword


def regenerate_symbol(keyword: str, user_data: UserData):
    """콜백 함수 - 완료 후 Streamlit이 자동으로 rerun함"""
    st.session_state.is_regenerating = True
    pair = process_keyword(keyword, user_data)
    st.session_state.is_regenerating = False


def single_symbol(pair: ImageTextPair, user_data: UserData, key_prefix: str = "", size_factor: float = 1.0):
    """
    단일 심볼을 카드 형태로 표시한다.
    key_prefix: 동일 심볼이 여러 위치에서 렌더링될 때 key 중복 방지용
    """
    with st.container(
        border=True,
        width=int(200 * size_factor),
        height=int(240 * size_factor),
        horizontal_alignment="center",
    ):
        st.image(pair.image, width="stretch", output_format="PNG")

        is_regenerating = st.session_state.get("is_regenerating", False)

        display_label = re.sub(r'\s*\([^)]*\)', '', pair.text).strip()

        clicked = st.button(
            display_label or pair.text,
            on_click=regenerate_symbol,
            args=(pair.text, user_data),
            disabled=is_regenerating,
            key=f"regenerate_{key_prefix}_{pair.text}",
        )


def gallery(user_data: UserData):
    """
    저장된 심볼들을 갤러리 형태로 표시한다.
    """
    gallery = user_data.symbol_gallery
    items = list(gallery.items())

    # 4개씩 아이템을 묶어 행(row) 단위로 처리
    # Streamlit에서 그리드 뷰를 구현하는 표준적인 패턴임
    for i in range(0, len(items), 4):
        cols = st.columns(4)
        row_items = items[i : i + 4]

        for col, (_key, pair) in zip(cols, row_items):
            with col:
                single_symbol(pair, user_data, key_prefix="gallery")

    
