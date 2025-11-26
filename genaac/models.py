# genaac/models/token.py

from typing import List, Optional, Dict
import base64

import pandas as pd
from pydantic import BaseModel, field_serializer, field_validator

from genaac.utils import png_to_url


class Token(BaseModel):
    keyword: str
    query: Optional[str] = None

    def __str__(self):
        return self.keyword if self.query is None else f"{self.keyword} ({self.query})"
    

class TokenPromptPair(BaseModel):
    token: Token
    prompt: str

    def to_shot(self) -> List[Dict]:
        return [
            {"role": "user", "content": str(self.token)},
            {"role": "assistant", "content": self.prompt}
        ]


class TokenPromptImagePair(TokenPromptPair):
    image: bytes

    def to_image_url(self) -> str:
        return png_to_url(self.image)
    

    # JSON 직렬화시 bytes를 base64 문자열로 변환
    @field_serializer('image')
    def serialize_image(self, value: bytes) -> str:
        return base64.b64encode(value).decode('utf-8')
    

    # JSON 역직렬화시 base64 문자열을 bytes로 변환
    @field_validator('image', mode='before')
    @classmethod
    def validate_image(cls, value):
        if isinstance(value, str):
            return base64.b64decode(value)
        return value


class TokenizingResponse(BaseModel):
    tokens: List[Token]
    

class EditingResponse(BaseModel):
    answer_to_user: str
    prompt: str



class EditingTurn(BaseModel):
    user_feedback: str
    response: EditingResponse
    result: TokenPromptImagePair


class EditingHistory(BaseModel):
    initial_pair: TokenPromptImagePair
    history: Optional[List[EditingTurn]] = list()


    def add_turn(self, turn: EditingTurn):
        self.history.append(turn)


    def history_to_messages(self) -> List[Dict]:
        messages = []

        messages.append({"role": "user", "content": [
            {"type": "text", "text": f"Original Token: {self.initial_pair.token}\nOriginal Prompt: {self.initial_pair.prompt}\nOriginal Image: "},
            {"type": "image_url", "image_url": {"url": png_to_url(self.initial_pair.image)}}
        ]})

        for turn in self.history:
            messages.append({"role": "user", "content": turn.user_feedback})
            messages.append({"role": "assistant", "content": turn.response.model_dump_json()})
            messages.append({"role": "user", "content": [
                {"type": "text", "text": f"Edited Token: {turn.result.token}\nEdited Prompt: {turn.result.prompt}\nEdited Image: "},
                {"type": "image_url", "image_url": {"url": png_to_url(turn.result.image)}}
            ]})

        return messages

    def get_final_pair(self) -> TokenPromptImagePair:
        if self.history:
            return self.history[-1].result
        else:
            return self.initial_pair



class SentencePair(BaseModel):
    sentence: str
    pairs: List[TokenPromptImagePair]

    def to_df(self):
        rows = [
            {
                "keyword": pair.token.keyword,
                "image": pair.to_image_url()
            }
            for pair in self.pairs
        ]

        return pd.DataFrame(rows)
