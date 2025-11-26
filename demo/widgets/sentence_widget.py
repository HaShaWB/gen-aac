# demo/widgets/sentence_widget.py

import streamlit as st

from genaac import tokenize, token_imaging_batch
from genaac.models import SentencePair, EditingHistory


# 임시 Few Shot -> 이후에는 자동 Few Shot (RAG) 추가 예정
FEW_SHOTS_SYMBOLS = {"좋아", "싫어", "먹다", "물음"} 


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

    sentence = st.chat_input("문장 입력", disabled=is_sentence_generating)
    st.session_state.sentence = sentence


    few_shots = [
        history.get_final_pair()
        for history in st.session_state.user_data.gallery
        if history.get_final_pair().token.keyword in FEW_SHOTS_SYMBOLS
    ]

    if sentence:
        st.session_state["is_sentence_generating"] = True

        with st.spinner("문장 변환 중입니다"):
            print(f"[Sentence Widget] Tokenizing sentence: {sentence}")
            pairs = tokenize(sentence).tokens
            print(f"[Sentence Widget] Imaging Keywords: " + ", ".join([pair.keyword for pair in pairs]))
            t_pairs = token_imaging_batch(pairs, few_shots=few_shots)
            print(f"[Sentence Widget] Finished Sentence: {sentence}")
            sentence_pair = SentencePair(sentence=sentence, pairs=t_pairs)

        st.session_state.sentence_pair = sentence_pair
        st.session_state.is_sentence_generating = False


    if st.session_state.get("sentence_pair", False):
        st.success(f"변환 완료: {st.session_state.sentence_pair.sentence}")
        sentence_pair = st.session_state.sentence_pair


        n_of_symbols = len(sentence_pair.pairs)

        cols = st.columns(n_of_symbols)

        for col, pair in zip(cols, sentence_pair.pairs):
            col.image(pair.image, width=120)
            col.subheader(pair.token.keyword)


        with st.expander("상세 보기"):

            df = sentence_pair.to_df()

            df["Stared"] = [False] * len(df)

            data = st.data_editor(
                df,
                height="stretch",
                row_height=120,
                column_config={"image": st.column_config.ImageColumn("AAC Image")}
            )

            clicked = st.button("Save Stared Symbols")

            if clicked:
                for idx, row in data.iterrows():
                    if row["Stared"]:
                        st.session_state.user_data.add_history(
                            EditingHistory(initial_pair=sentence_pair.pairs[idx])
                        )
                
                st.session_state.user_data.upload_to_server()
                st.success("Saved Stared Symbols")
                print(f"[Sentence Widget] Saved Stared Symbols")