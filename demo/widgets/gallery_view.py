# demo/widgets/gallery_view.py

import streamlit as st
from st_clickable_images import clickable_images

from genaac.models import EditingHistory


def symbol_view(index: int):
    user_data = st.session_state.user_data
    history: EditingHistory = user_data.gallery[index]

    st.header(history.get_final_pair().token.keyword)

    left, right = st.columns(2)

    with left:
        clicked_left = st.button("삭제")
        if clicked_left:
            if len(user_data.gallery) == 1:
                st.error("최소 1개의 심볼이 있어야 합니다")
                return
            user_data.pop_history(index)
            user_data.upload_to_server()
            st.success("심볼 삭제 완료")
            st.rerun()
    
    with right:
        clicked_right = st.button("기록 초기화")
        if clicked_right:
            history.history = list()
            user_data.upload_to_server()
            st.success("기록 초기화 완료")
            st.rerun()




    st.image(history.get_final_pair().to_image_url(), width=120)


    for turn in history.history:
        with st.chat_message("user"):
            st.write(turn.user_feedback)
        
        with st.chat_message("assistant"):
            st.write(turn.response.answer_to_user)
            st.image(turn.result.to_image_url(), width=120)
    


def gallery_view():

    st.set_page_config(
        page_title="GenAAC Gallery",
        layout="wide",
    )


    user_data = st.session_state.user_data
    gallery= user_data.gallery

    
    st.session_state.gallery_selected_idx = st.session_state.get("gallery_selected_idx", -1)

    
    _, left, right, _ = st.columns([1, 3, 1, 1])

    with left:
        st.title("GenAAC")
        st.header("GenAAC Gallery")
        st.markdown("""
        아래 갤러리에서 사용자님이 저장한 키워드와 심볼을 확인할 수 있습니다. (기본 제공 키워드 포함)

        심볼을 클릭하여 더 자세한 설명을 확인하고, 심볼을 삭제, 수정할 수 있습니다.
        이 키워드들은 향후 사용자님이 문장을 변환할 때 우선하여 사용되게됩니다.
        """)
        clicked = clickable_images(
            [history.get_final_pair().to_image_url() for history in gallery],
            titles=[history.get_final_pair().token.keyword for history in gallery],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "10px", "width": "120px", "height": "120px"},
        )

        if clicked >= 0:
            st.session_state.gallery_selected_idx = clicked

    with right:
        if st.session_state.gallery_selected_idx >= 0:
            symbol_view(st.session_state.gallery_selected_idx)
