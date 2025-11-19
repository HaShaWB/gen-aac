# genaac/models/token.py

from typing import List, Optional

from pydantic import BaseModel


class Token(BaseModel):
    keyword: str
    query: Optional[str] = None

    def __str__(self):
        return self.keyword if self.query is None else f"{self.keyword} ({self.query})"
    

class TokenPromptPair(Token):
    prompt: str


class TokenPromptImagePair(TokenPromptPair):
    image: bytes



class TokenizingResponse(BaseModel):
    tokens: List[Token]
    