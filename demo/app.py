# demo/app.py

import streamlit as st

from demo.user_data import UserData
from demo.gallery import gallery, single_symbol
from demo.functions import process_sentence, process_image_keyword


st.session_state.user_data: UserData = UserData()
st.session_state.user_data.download_userdata()

st.set_page_config(page_title="AAC Symbol Generator", page_icon=":art:")

st.title("GenAAC Demo")
st.space("medium")

# 변환 모드 선택

SENTENCE_MODE = "일반 생성"
IMAGE_MODE = "사진을 통해 생성"

mode = st.radio(
    "변환 모드 선택",
    [SENTENCE_MODE, IMAGE_MODE],
    horizontal=True
)

st.space("small")


if mode == SENTENCE_MODE:
    # 문장 변환 UI
    sentence = st.text_input("AAC Symbol로 생성할 문장이나 단어를 입력해주세요.")
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


elif mode == IMAGE_MODE:
    # 이미지 변환 UI
    keyword = st.text_input("키워드를 입력해주세요.", placeholder="예: 강아지, 사과")
    
    # 이미지 입력 방식 선택 (탭)
    tab_upload, tab_camera = st.tabs(["📁 파일 업로드", "📷 카메라"])
    
    with tab_upload:
        uploaded_image = st.file_uploader(
            "참조 이미지를 업로드해주세요.",
            type=["png", "jpg", "jpeg", "webp"]
        )
    
    with tab_camera:
        camera_image = st.camera_input("사진을 촬영해주세요.")
    
    # 업로드 또는 카메라 중 하나 선택
    image = uploaded_image or camera_image
    
    button = st.button("AAC Symbol 생성")
    
    if button:
        if not keyword:
            st.error("키워드를 입력해주세요.")
        elif not image:
            st.error("이미지를 업로드하거나 촬영해주세요.")
        else:
            with st.spinner("AAC Symbol 생성 중..."):
                image_bytes = image.getvalue()
                pair = process_image_keyword(keyword, image_bytes, st.session_state.user_data)
                st.session_state.current_image_pair = pair
    
    # 생성된 심볼 표시
    if st.session_state.get("current_image_pair", False):
        st.subheader("생성된 AAC Symbol")
        single_symbol(st.session_state.current_image_pair, st.session_state.user_data, key_prefix="image_current", size_factor=1.5)

st.space("medium")
st.divider()
st.space("medium")

gallery(st.session_state.user_data)



st.write(f"user_id: {st.session_state.user_data.user_id}")