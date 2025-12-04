# genaac/symbol_generation.py

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from genaac.utils import nano_banana, ImageTextPair, file_to_bytes


ROOT_DIR = Path(__file__).parent.parent
SYMBOL_GENERATION_PROMPT = (ROOT_DIR / "prompts" / "symbol_generation.md").read_text(encoding="utf-8")
BASIC_SYMBOL_PAIRS_INFO = json.loads((ROOT_DIR / "prompts" / "basic_symbol_pairs.json").read_text(encoding="utf-8"))
BASIC_SYMBOL_PAIRS = [
    ImageTextPair(
        image=file_to_bytes(ROOT_DIR / "prompts" / f"{pair['keyword']}.png"),
        text=pair['instruction']
    )
    for pair in BASIC_SYMBOL_PAIRS_INFO
]


def symbol_generation(keyword: str) -> ImageTextPair:
    return nano_banana(
        prompt=f"키워드: {keyword}",
        system_instruction=SYMBOL_GENERATION_PROMPT,
        image_text_pairs=BASIC_SYMBOL_PAIRS
    )


def symbol_generation_batch(keywords: List[str], max_workers: int = 4) -> List[ImageTextPair]:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(symbol_generation, keywords))
    return results
    