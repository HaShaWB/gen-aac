# genaac/utils/llm_client.py

from pathlib import Path
from typing import Optional

import yaml
import litellm
from pydantic import BaseModel


ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG = yaml.safe_load((ROOT_DIR / "config.yaml").read_text(encoding="utf-8"))


primary_llm = CONFIG["model"]["primary_llm"]
secondary_llm = CONFIG["model"]["secondary_llm"]


def generate_llm_response(messages: list[dict], **kwargs) -> Optional[str]:
    try:
        response = litellm.completion(
            model=primary_llm,
            messages=messages,
            **kwargs,
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"[LLM] Error generating response with primary llm -> try secondary llm: {e}")
        try:
            response = litellm.completion(
            model=secondary_llm,
                messages=messages,
                **kwargs,
            )
            return response["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"[LLM] Error generating response with secondary llm -> return None: {e}")
            return None
    

def generate_llm_response_in_json(
    messages: list[dict], 
    schema: BaseModel, **kwargs) -> Optional[BaseModel]:

    try:
        response = generate_llm_response(messages, response_format=schema, **kwargs)
        return schema.model_validate_json(response)
    except Exception as e:
        print(f"[LLM] Error in validating json response: {e}")
        print(f"[LLM] Response: {response}")
        return None
