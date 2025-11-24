# genaac/token_imaging.py

from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor

from genaac.utils import generate_llm_response, generate_imagen_response
from genaac.models import TokenPromptPair, Token, TokenPromptImagePair


ROOT_DIR = Path(__file__).parent.parent
TOKEN_IMAGING_PROMPT = (ROOT_DIR / "prompts" / "token_imaging_prompt.md").read_text(encoding="utf-8")



def token_to_prompt(token: Token, few_shots: List[TokenPromptPair] = list()) -> str:

    messages = [{"role": "system", "content": TOKEN_IMAGING_PROMPT}] \
        + [shot.to_shot() for shot in few_shots] \
        + [{"role": "user", "content": str(token)}]

    response = generate_llm_response(messages)

    return response


def token_imaging(token: Token, few_shots: List[TokenPromptPair] = list()) -> TokenPromptImagePair:

    prompt = token_to_prompt(token, few_shots)
    image = generate_imagen_response(prompt)

    return TokenPromptImagePair(
        token=token,
        prompt=prompt,
        image=image
    )


def token_imaging_batch(
    tokens: List[Token], 
    few_shots: List[TokenPromptPair] = list(), 
    max_workers: int = 5
) -> List[TokenPromptImagePair]:
    
    def _process_single(token: Token) -> TokenPromptImagePair:
        return token_imaging(token, few_shots)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_process_single, tokens))
    
    return results
