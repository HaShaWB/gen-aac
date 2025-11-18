# genaac/utils/imagen_client.py

from pathlib import Path

import yaml
from google import genai


ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG = yaml.safe_load((ROOT_DIR / "config.yaml").read_text(encoding="utf-8"))


genai_client = genai.Client()


def generate_imagen_response(prompt: str) -> bytes:
    response = genai_client.models.generate_images(
        model=CONFIG["model"]["imagen"],
        prompt=prompt
    )

    if not response.images:
        print(f"[IMAGEN] Error generating imagen response: {response}")
        return None
    
    return response.generated_images[0].image.image_bytes
