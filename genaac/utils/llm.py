# genaac/utils/llm_client.py

from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

import litellm
from pydantic import BaseModel

from genaac.config import CONFIG


PRIMARY_LLM = CONFIG["model"]["primary_llm"]
SECONDARY_LLM = CONFIG["model"]["secondary_llm"]


def generate_llm_response(messages: list[dict],
    primary_llm: str = PRIMARY_LLM,
    secondary_llm: str = SECONDARY_LLM,
    **kwargs) -> Optional[str]:
    try:
        response = litellm.completion(
            model=primary_llm,
            messages=messages,
            drop_params=True,
            **kwargs,
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"[LLM] Error generating response with primary llm -> try secondary llm: {e}")
        try:
            response = litellm.completion(
            model=secondary_llm,
                messages=messages,
                drop_params=True,
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
        response = generate_llm_response(messages, response_format=schema, drop_params=True, **kwargs)
        return schema.model_validate_json(response)
    except Exception as e:
        print(f"[LLM] Error in validating json response: {e}")
        print(f"[LLM] Response: {response}")
        return None



def generate_llm_response_parallel(
    messages_list: List[List[dict]],
    max_workers: int = 5,
    **kwargs
) -> List[Optional[str]]:
    results = [None] * len(messages_list)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(generate_llm_response, messages, **kwargs): idx
            for idx, messages in enumerate(messages_list)
        }
        
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"[LLM] Parallel processing error at index {idx}: {e}")
                results[idx] = None
    
    return results



def generate_llm_response_in_json_parallel(
    messages_list: List[List[dict]],
    schema: BaseModel,
    max_workers: int = 5,
    **kwargs
) -> List[Optional[BaseModel]]:
    results = [None] * len(messages_list)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(generate_llm_response_in_json, messages, schema, drop_params=True, **kwargs): idx
            for idx, messages in enumerate(messages_list)
        }
        
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"[LLM] Parallel processing error at index {idx}: {e}")
                results[idx] = None
    
    return results
