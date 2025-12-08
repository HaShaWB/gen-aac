# demo/widgets/gallery.py

import re
import streamlit as st


def gallery():
    user_data = st.session_state.user_data
    gallery = user_data.symbol_gallery

    # 4열 배치를 위해 아이템들을 리스트로 변환
    items = list(gallery.items())
    
    # 4개씩 묶어서 행 단위로 처리
    for row_start in range(0, len(items), 4):
        cols = st.columns(4)
        row_items = items[row_start:row_start + 4]
        
        for col_idx, (keyword, pair) in enumerate(row_items):
            with cols[col_idx]:
                with st.container(
                    border=True,
                    width=240,
                    height=240,
                    horizontal_alignment="center",
                    # vertical_alignment="center",
                ):
                    st.image(pair.image, width="stretch", output_format="PNG")
                    
                    # 재생성 중인지 확인
                    is_regenerating = st.session_state.get("regenerating", False)
                    
                    # 괄호 내용은 툴팁으로 분리 (레이아웃 진동 방지)
                    display_label = re.sub(r'\s*\([^)]*\)', '', keyword).strip()
                    
                    clicked = st.button(
                        label=display_label or keyword,
                        help=keyword if display_label != keyword else None,
                        width="stretch",
                        disabled=is_regenerating,
                        key=f"gallery_btn_{hash(keyword)}"
                    )
                    if clicked:
                        st.session_state["regenerating"] = True
                        st.session_state["regenerating_keyword"] = keyword
                        st.rerun()
                    
                    # 재생성 실행 (별도 블록에서 처리)
                    if is_regenerating and st.session_state.get("regenerating_keyword") == keyword:
                        with st.spinner("Symbol 재생성 중..."):
                            user_data.regenerate_symbol(keyword, converting_keyword=False)
                            st.session_state["regenerating"] = False
                            st.session_state.pop("regenerating_keyword", None)
                            st.rerun()
                    