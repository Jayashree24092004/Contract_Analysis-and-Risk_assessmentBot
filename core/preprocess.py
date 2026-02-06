import re
from langdetect import detect
from typing import Literal

Lang = Literal["en", "hi"]


def detect_language(text: str) -> Lang:
    try:
        code = detect(text[:5000])
    except Exception:
        code = "en"
    return "hi" if code.startswith("hi") else "en"


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def normalize_for_nlp(text: str, lang: Lang, llm_client) -> str:
    if lang == "en":
        return text
    # Hindi -> English normalization
    prompt = (
        "You are given a Hindi commercial contract. "
        "Translate it to neutral, literal English for NLP processing. "
        "Do not add or remove information."
    )
    return llm_client.translate_contract(text, prompt)
