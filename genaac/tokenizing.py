# genaac/tokenizing.py

from typing import List, Literal

from pydantic import BaseModel

from genaac.config import TOKENIZING_PROMPT
from genaac.utils import generate_llm_response_in_json

class Token(BaseModel):
    keyword: str
    syntax: Literal["None", "부정", "의문"]

class Tokens(BaseModel):
    tokens: List[Token]


def tokenizing(sentence: str) -> List[Token]:
    messages = [
        {"role": "system", "content": TOKENIZING_PROMPT},
        {"role": "user", "content": sentence}
    ]

    response = generate_llm_response_in_json(messages, Tokens)

    print(f"[TOKENIZING] Tokenizing Ended: {sentence} -> {response}")

    return response.tokens
