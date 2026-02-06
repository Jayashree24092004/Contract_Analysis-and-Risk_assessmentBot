import spacy

# ===============================
# English NLP (Required)
# ===============================
try:
    NLP_EN = spacy.load("en_core_web_sm")
except OSError as e:
    raise RuntimeError(
        "English SpaCy model not found.\n"
        "Please run:\n"
        "    python -m spacy download en_core_web_sm"
    ) from e

# ===============================
# Hindi NLP (Optional)
# SpaCy v3.8.x does NOT provide
# hi_core_news_sm, so keep safe
# ===============================
NLP_HI = None
