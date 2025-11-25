# demo/widgets/sentence_widget.py

import streamlit as st

from genaac import tokenize, token_imaging_batch
from genaac.models import SentencePair, EditingHistory


def sentence_widget():
    
    st.title("GenAAC")
    st.header("문장 변환: 문장 -> GenAAC Symbols")

    st.markdown("""
    ### 사용 방법
    GenAAC는 일상 문장을 *(1) 적절한 단위로 분할 및 재구성*하고, *(2) 각 단위를 AAC Symbol로 변환*합니다.

    생성형 인공지능을 이용하여 대부분의 문장을 처리할 수 있으나, 더 효과적인 사용을 위해 다음을 참고해주세요.

    1. 하나의 문장에는 하나의 의미 또는 의도만 담아주세요.
    2. 시적이고 다채로운 표현보단 명확하고 직관적인 표현을 사용해주세요.
    3. 본 GenAAC 시스템은 아직 개발 중입니다. 참고 용도로만 사용해주세요.
    4. 기타 문의 및 제안은 개발자의 이메일(whitebluej@kaist.ac.kr)로 연락주세요.
    
    """)

    st.divider()

    is_sentence_generating = st.session_state.get("is_sentence_generating", False)

    sentence = st.text_input("문장 입력", disabled=is_sentence_generating)
    st.session_state.sentence = sentence

    if sentence:
        st.session_state["is_sentence_generating"] = True

        with st.spinner("문장 변환 중입니다"):
            pairs = tokenize(sentence)
            t_pairs = token_imaging_batch(pairs.tokens)
            sentence_pair = SentencePair(sentence=sentence, pairs=t_pairs)

        st.session_state.sentence_pair = sentence_pair
        st.session_state.is_sentence_generating = False

        st.rerun()


    if st.session_state.get("sentence_pair", False):
        st.success(f"변환 완료: {st.session_state.sentence_pair.sentence}")
        sentence_pair = st.session_state.sentence_pair

        df = sentence_pair.to_df()

        df["Stared"] = [False] * len(df)


        clicked = st.data_editor(
            df,
            height="stretch",
            row_height=120,
            column_config={"image": st.column_config.ImageColumn("AAC Image")}
        )

        clicked = st.button("Save Stared Symbols")

        if clicked:
            for idx, row in clicked.iterrows():
                if row["Stared"]:
                    st.session_state.user_data.add_history(
                        EditingHistory(initial_pair=sentence_pair.pairs[idx])
                    )
            
            st.session_state.user_data.upload_to_server()

            st.rerun()