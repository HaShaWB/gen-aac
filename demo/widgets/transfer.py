# demo/widgets/transfer.py

import streamlit as st


def aac_from_keyword():
    """단어 변환 위젯"""
    col1, col2 = st.columns([4, 1])
    with col1:
        chat = st.text_input("변환할 단어를 입력해주세요.")
    with col2:
        st.write("")  # 버튼 높이 맞춤용 빈 공간
        button = st.button("변환")

    if button or chat:
        with st.spinner("Symbol 생성 중..."):
            pair = st.session_state.user_data.find_or_generate_symbol(chat)
            st.image(pair.image, width=320, output_format="PNG")
            st.header(pair.text)

    elif button and not chat:
        st.error("단어를 입력해주세요.")


def aac_from_image():
    """이미지 변환 위젯 - session_state로 파일 상태 유지"""
    # file_uploader는 form 밖에서 처리 (form 내부에선 submit 시 리셋됨)
    image = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"], key="aac_from_image_uploader")

    # 파일이 업로드되면 session_state에 저장
    if image is not None:
        st.session_state["uploaded_image_bytes"] = image.getvalue()

    col1, col2 = st.columns([4, 1])
    with col1:
        chat = st.text_input("변환할 단어를 입력해주세요.", key="aac_from_image_chat")
    with col2:
        st.write("")
        button = st.button("변환", key="aac_from_image_button")

    # 저장된 이미지 바이트 가져오기
    image_bytes = st.session_state.get("uploaded_image_bytes")

    if button:
        if chat and image_bytes:
            with st.spinner("Symbol 생성 중..."):
                pair = st.session_state.user_data.regenerate_symbol_from_image(chat, image_bytes)
                st.image(pair.image, width=320, output_format="PNG")
                st.header(pair.text)
        else:
            st.error("단어와 이미지를 입력해주세요.")
