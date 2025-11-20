# genaac/models/token.py

from typing import List, Optional, Dict

from pydantic import BaseModel


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



class TokenizingResponse(BaseModel):
    tokens: List[Token]
    