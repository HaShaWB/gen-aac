# genaac/special_token_processing.py

from genaac.utils import ImageTextPair, file_to_bytes, ImageTextPair, generate_banana_response
from genaac.config import ROOT_DIR, AAC_FROM_IMAGE_PROMPT
from typing import Literal, List

EATING_SYMBOL = file_to_bytes(ROOT_DIR / "templates" / "eating.png")
GOING_SYMBOL = file_to_bytes(ROOT_DIR / "templates" / "going.png")

EATING_PAIR = ImageTextPair(image=EATING_SYMBOL, text="Keyword: 먹다. 그림 상의 빨간 점선 위에 먹을 대상을 올려야한다. 이때, 합성 후 기존 빨간 점선은 제거한다.")
GOING_PAIR = ImageTextPair(image=GOING_SYMBOL, text="Keyword: 가다. 그림 상의 검은 점선 사각형 안에 갈 곳을 그려야한다. 이때, 합성 후 기존 검은 점선은 제거한다.")


def aac_collage(main_keyword: Literal["eat", "go"], sub_keyword_pair: ImageTextPair) -> ImageTextPair:
    if main_keyword == "eat": 
        main_pair = EATING_PAIR
    elif main_keyword == "go":
        main_pair = GOING_PAIR
    else:
        raise ValueError(f"Invalid main keyword: {main_keyword}")

    messages = [
        {"role": "system", "content": AAC_FROM_IMAGE_PROMPT},
        main_pair.to_chat(),
        sub_keyword_pair.to_chat()
    ]

    response = generate_banana_response(messages)
    response.text = f"{sub_keyword_pair.text} / {main_keyword}"
    return response


