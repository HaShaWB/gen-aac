   # genaac/convert_keyword.py

from typing import List

from genaac.utils import generate_llm_response, generate_llm_response_parallel
from genaac.config import CONFIG

PRIMARY_KEYWORD_LLM = CONFIG["model"]["primary_keyword_llm"]
SECONDARY_KEYWORD_LLM = CONFIG["model"]["secondary_keyword_llm"]

INSTRUCTION = """## Persona

너는 유저가 입력한 키워드를 적절한 형태를 가공해야해. 유저가 입력한 키워드를 표준어, 기본형으로 변환하는거야. 
이때, 동음이의어 문제를 피하기 위해 키워드 뒤에 괄호에 영어 단어를 적어줘. 구체적으로 다음의 변환 방법을 따라줘.

## Examples

- '학교' -> '학교(school)'
- '치킨' -> '치킨(chicken)'
- '갔다' -> '가다(go)'
- '배 (타는 배)' -> '배(ship)'
- '배 - 이동수단' -> '배(ship)'
"""


def convert_keyword(keyword: str) -> str:
    messages = [
        {"role": "system", "content": INSTRUCTION},
        {"role": "user", "content": keyword}
    ]

    response = generate_llm_response(
        messages,
        primary_llm=PRIMARY_KEYWORD_LLM,
        secondary_llm=SECONDARY_KEYWORD_LLM
    )

    print(f"[CONVERT KEYWORD] {keyword} -> {response}")

    return response if response else keyword


def convert_keyword_parallel(keywords: List[str]) -> List[str]:
    messages_list = [
        [
            {"role": "system", "content": INSTRUCTION}, 
            {"role": "user", "content": keyword}
        ] 
        for keyword in keywords
    ]

    response = generate_llm_response_parallel(
        messages_list,
        primary_llm=PRIMARY_KEYWORD_LLM,
        secondary_llm=SECONDARY_KEYWORD_LLM,
    )
    
    print(f"[CONVERT KEYWORD PARALLEL] {keywords} -> {response}")

    return [response if response else keyword for response, keyword in zip(response, keywords)]