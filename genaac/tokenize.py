# genaac/tokenize.py

from pathlib import Path

from genaac.utils import generate_llm_response_in_json
from genaac.models import TokenizingResponse


ROOT_DIR = Path(__file__).parent.parent
TOKENIZING_PROMPT = (ROOT_DIR / "prompts" / "tokenizing_prompt.md").read_text(encoding="utf-8")


def tokenize(sentence: str) -> TokenizingResponse:
    response = generate_llm_response_in_json(
        [
            {"role": "system", "content": TOKENIZING_PROMPT},
            {"role": "user", "content": sentence},
        ],
        TokenizingResponse,
    )
    return response
    