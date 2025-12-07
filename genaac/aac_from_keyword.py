# genaac/aac_from_keyword.py

from typing import List

from genaac.config import AAC_FROM_KEYWORD_PROMPT
from genaac.utils import (
    generate_banana_response,
    generate_banana_response_parallel,
    ImageTextPair,
)
from genaac.convert_keyword import convert_keyword, convert_keyword_parallel


def aac_from_keyword(keyword: str, converting_keyword: bool = True) -> ImageTextPair:
    if converting_keyword:
        keyword = convert_keyword(keyword)

    messages = [
        {"role": "system", "content": AAC_FROM_KEYWORD_PROMPT},
        {"role": "user", "content": f"키워드: {keyword}"}
    ]

    response = generate_banana_response(messages)
    response.text = keyword
    
    print(f"[AAC FROM KEYWORD] Generated: {keyword}")

    return response


def aac_from_keyword_parallel(
    keywords: List[str], 
    converting_keyword: bool = True, 
    max_workers: int = 5
) -> List[ImageTextPair]:

    if converting_keyword:
        keywords = convert_keyword_parallel(keywords)

    messages_list = [
        [
            {"role": "system", "content": AAC_FROM_KEYWORD_PROMPT},
            {"role": "user", "content": f"키워드: {keyword}"}
        ]
        for keyword in keywords
    ]

    print(f"[AAC FROM KEYWORD PARALLEL] Generated: {keywords}")

    pairs = generate_banana_response_parallel(messages_list, max_workers=max_workers)
    for pair, keyword in zip(pairs, keywords):
        pair.text = keyword
    return pairs
