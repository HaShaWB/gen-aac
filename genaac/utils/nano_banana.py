# genaac/utils/nano_banana.py

from typing import Optional, List

import litellm
from pydantic import BaseModel

from genaac.utils import bytes_to_url, url_to_bytes


class ImageTextPair(BaseModel):
    image: bytes
    text: Optional[str] = None

    def to_chat(self, role: str = "user") -> dict:
        return {
            "role": role,
            "content": [
                {"type": "text", "text": self.text},
                {"type": "image_url", "image_url": {"url": bytes_to_url(self.image)}}
            ]
        }


def nano_banana(
    prompt: str,
    system_instruction: Optional[str] = None,
    image_text_pairs: Optional[List[ImageTextPair]] = None,
) -> ImageTextPair:
    messages = []

    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    
    if image_text_pairs:
        for image_text_pair in image_text_pairs:
            messages.append(image_text_pair.to_chat())
    
    messages.append({"role": "user", "content": prompt})
    
    response = litellm.completion(
        model="openrouter/google/gemini-3-pro-image-preview",
        messages=messages,
        modalities=["text", "image"],
    )
    message = response.choices[0].message

    text = message.content
    image = message.images[-1]['image_url']['url']
    image = url_to_bytes(image)

    return ImageTextPair(image=image, text=text)
    