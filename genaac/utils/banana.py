# genaac/utils/banana.py

from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from litellm import completion
from pydantic import BaseModel

from genaac.config import CONFIG
from genaac.utils import bytes_to_url, url_to_bytes, bytes_to_image


primary_banana = CONFIG["model"]["primary_banana"]
secondary_banana = CONFIG["model"]["secondary_banana"]


class ImageTextPair(BaseModel):
    image: bytes
    text: Optional[str] = None

    def to_chat(self, role: Optional[str] = "user") -> dict:

        if self.text:
            return {
                "role": role,
                "content": [
                    {"type": "text", "text": self.text},
                    {"type": "image_url", "image_url": {"url": bytes_to_url(self.image)}},
                ]
            }
            
        else:
            return {
                "role": role,
                "content": [
                    {"type": "image_url", "image_url": {"url": bytes_to_url(self.image)}},
                ]
            }


    
    def show(self):
        bytes_to_image(self.image).show()


def generate_banana_response(messages: List[dict], **kwargs) -> ImageTextPair:
    try:
        response = completion(
            model=primary_banana,
            messages=messages,
            extra_body={"modalities": ["image", "text"]},
            **kwargs,
        )

        response = response.choices[0].message

        return ImageTextPair(
            image=url_to_bytes(response.images[-1]["image_url"]["url"]),
            text=response.content,
        )

    except Exception as e:
        print(f"[BANANA] Error generating response with primary banana -> try secondary banana: {e}")
        try:
            response = completion(
                model=secondary_banana,
                messages=messages,
                extra_body={"modalities": ["image", "text"]},
                **kwargs,
            )
            response = response.choices[0].message
            return ImageTextPair(
                image=url_to_bytes(response.images[-1]["image_url"]["url"]),
                text=response.content,
            )
        except Exception as e:
            print(f"[BANANA] Error generating response with secondary banana -> return None: {e}")
            return None



def generate_banana_response_parallel(
    messages_list: List[List[dict]], 
    max_workers: int = 5,
    **kwargs
) -> List[Optional[ImageTextPair]]:
    results = [None] * len(messages_list)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 인덱스와 함께 future 생성
        future_to_idx = {
            executor.submit(generate_banana_response, messages, **kwargs): idx
            for idx, messages in enumerate(messages_list)
        }
        
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"[BANANA] Parallel processing error at index {idx}: {e}")
                results[idx] = None
    
    return results
