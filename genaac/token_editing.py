# genaac/token_editing.py

from pathlib import Path
from typing import List

from genaac.utils import generate_llm_response_in_json, generate_imagen_response
from genaac.models import EditingResponse, EditingTurn, EditingHistory, TokenPromptImagePair


ROOT_DIR = Path(__file__).parent.parent
TOKEN_EDITING_PROMPT = (ROOT_DIR / "prompts" / "token_editing_prompt.md").read_text(encoding="utf-8")



def edit_token(history: EditingHistory, user_feedback: str) -> EditingTurn:
    messages = [{"role": "system", "content": TOKEN_EDITING_PROMPT}] \
        + history.history_to_messages() \
        + [{"role": "user", "content": user_feedback}]

    response: EditingResponse = generate_llm_response_in_json(messages, EditingResponse)

    image = generate_imagen_response(response.prompt)

    turn = EditingTurn(
        user_feedback=user_feedback,
        response=response,
        result=TokenPromptImagePair(
            token=history.initial_pair.token,
            prompt=response.prompt,
            image=image
        )
    )

    return turn
