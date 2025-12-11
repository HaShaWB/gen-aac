# genaac/config.py

from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
CONFIG = yaml.safe_load((ROOT_DIR / "config.yaml").read_text(encoding="utf-8"))

load_dotenv(ROOT_DIR / ".env")


AAC_SYMBOL_GUIDELINE = (ROOT_DIR / "prompt" / "aac_symbol_guideline.md").read_text(encoding="utf-8")

AAC_FROM_IMAGE_PROMPT = (ROOT_DIR / "prompt" / "aac_from_image.md").read_text(encoding="utf-8")
AAC_FROM_IMAGE_PROMPT = AAC_FROM_IMAGE_PROMPT.replace("{{ aac_symbol_guideline }}", AAC_SYMBOL_GUIDELINE)

AAC_FROM_KEYWORD_PROMPT = (ROOT_DIR / "prompt" / "aac_from_keyword.md").read_text(encoding="utf-8")
AAC_FROM_KEYWORD_PROMPT = AAC_FROM_KEYWORD_PROMPT.replace("{{ aac_symbol_guideline }}", AAC_SYMBOL_GUIDELINE)

TOKENIZING_PROMPT = (ROOT_DIR / "prompt" / "tokenizing.md").read_text(encoding="utf-8")
