# genaac/tokenizing.py

from typing import List

from pydantic import BaseModel

from genaac.config import TOKENIZING_PROMPT
from genaac.utils import generate_llm_response_in_json

class Token(BaseModel):
    keyword: str
    type: str
    syntax: str


def tokenizing(sentence: str) -> List[Token]:
    messages = [
        {"role": "system", "content": TOKENIZING_PROMPT},
        {"role": "user", "content": sentence}
    ]

    response = generate_llm_response_in_json(messages, Token)
    return response
