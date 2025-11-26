# demo/widgets/login.py

import streamlit as st

from user_data import UserData


@st.dialog("로그인", dismissible=False)
def login():
    st.title("GenAAC")
    st.subheader("환영합니다! 데이터 관리를 위해 고유한 ID를 입력해주세요")

    user_id = st.text_input("ID", placeholder="대소문자와 띄어쓰기를 구분합니다")

    st.write("데이터는 암호화되지 **않습니다**. 민감한 정보를 입력하지 마세요")

    if user_id:
        st.session_state.user_id = user_id

        user_data = UserData.from_server(user_id)

        if user_data:
            st.session_state.user_data = user_data
            st.success(f"로그인 성공: {user_id}")
            st.rerun()

        else:
            st.session_state.user_data = UserData.from_server("default")
            st.session_state.user_data.user_id = user_id
            st.warning(f"새로운 사용자 생성: {user_id}")
            st.session_state.user_data.upload_to_server()
            st.rerun()

