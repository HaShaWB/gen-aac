# demo/widgets/gallery_view.py

import streamlit as st
from st_clickable_images import clickable_images

from genaac import token_imaging, edit_token
from genaac.models import EditingHistory, Token


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
            st.session_state.gallery_selected_idx = -1
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
    
    feedback = st.chat_input("수정하고 싶은 점을 입력해주세요")

    if feedback:
        with st.spinner("심볼 수정 중입니다"):
            turn = edit_token(history, feedback)
            history.add_turn(turn)
            user_data.upload_to_server()
            st.success("심볼 수정 완료")
            st.rerun()



    
@st.dialog("Add New", dismissible=False)
def new_symbol():
    st.header("새로운 심볼 추가하기")

    keyword = st.text_input("Keyword", placeholder="1~2 단어의 키워드")
    query = st.text_input("Query", placeholder="해당 키워드의 문맥상, 사전상의 의미를 설명하는 문장")

    left, right = st.columns(2)

    gallery_generating = st.session_state.get("gallery_generating", False)

    with left:
        clicked_left = st.button("생성", disabled=gallery_generating)
    with right:
        clicked_right = st.button("취소", disabled=gallery_generating)

    if clicked_left: 
        if not keyword or not query:
            st.error("키워드와 쿼리를 입력해주세요")
            
        else:
            st.session_state.gallery_generating = True
            with st.spinner("새로운 심볼 추가 중입니다"):
                token = Token(keyword=keyword, query=query)

                pair = token_imaging(token)

                history = EditingHistory(initial_pair=pair)

                st.session_state.user_data.add_history(history)
                st.session_state.user_data.upload_to_server()
                st.success("새로운 심볼 추가 완료")
            st.session_state.gallery_generating = False
            st.rerun()

    if clicked_right:
        return


def gallery_view():
    # set_page_config는 app.py에서 한 번만 호출
    user_data = st.session_state.user_data
    gallery= user_data.gallery

    
    st.session_state.gallery_selected_idx = st.session_state.get("gallery_selected_idx", -1)

    
    left, right = st.columns([3, 2])

    with left:
        st.title("GenAAC")
        st.header("GenAAC Gallery")
        st.markdown("""
        아래 갤러리에서 사용자님이 저장한 키워드와 심볼을 확인할 수 있습니다. 
        (기본 제공 키워드 포함)

        심볼을 클릭하여 더 자세한 설명을 확인하고, 심볼을 삭제, 수정할 수 있습니다.
        이 키워드들은 향후 사용자님이 문장을 변환할 때 우선하여 사용되게됩니다.
        """)

        clicked_new = st.button("새로운 심볼 추가")

        if clicked_new:
            new_symbol()

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
