# genaac/aac_from_keyword.py

from typing import List

from genaac.config import AAC_FROM_KEYWORD_PROMPT, ROOT_DIR
from genaac.utils import (
    generate_banana_response,
    generate_banana_response_parallel,
    ImageTextPair,
    file_to_bytes,
)

HUMAN_SYMBOL = ImageTextPair(
    image=file_to_bytes(ROOT_DIR / "templates" / "human.png"),
    text="예시: '사람' \n주어진 이미지는 사람을 나타내는 AAC Symbol이야. 키워드에 사람이 들어간다면 참고해."
)

def aac_from_keyword(keyword: str) -> ImageTextPair:

    messages = [
        {"role": "system", "content": AAC_FROM_KEYWORD_PROMPT},
        HUMAN_SYMBOL.to_chat(),
        {"role": "user", "content": f"키워드: {keyword}"}
    ]

    response = generate_banana_response(messages)
    response.text = keyword
    
    print(f"[AAC FROM KEYWORD] Generated: {keyword}")

    return response


def aac_from_keyword_parallel(
    keywords: List[str],
    max_workers: int = 5
) -> List[ImageTextPair]:

    messages_list = [
        [
            {"role": "system", "content": AAC_FROM_KEYWORD_PROMPT},
            HUMAN_SYMBOL.to_chat(),
            {"role": "user", "content": f"키워드: {keyword}"}
        ]
        for keyword in keywords
    ]

    print(f"[AAC FROM KEYWORD PARALLEL] Generated: {keywords}")

    pairs = generate_banana_response_parallel(messages_list, max_workers=max_workers)
    for pair, keyword in zip(pairs, keywords):
        pair.text = keyword
    return pairs
