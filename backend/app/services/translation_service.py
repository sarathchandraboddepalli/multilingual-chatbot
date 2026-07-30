SAMPLE_TRANSLATIONS = {
    ("en", "te"): {
        "hello": "నమస్కారం",
        "scheme": "పథకం",
        "pension": "పెన్షన్",
        "how": "ఎలా",
        "apply": "దరఖాస్తు చేయండి",
    },
    ("en", "hi"): {
        "hello": "नमस्ते",
        "scheme": "योजना",
        "pension": "पेंशन",
        "how": "कैसे",
        "apply": "आवेदन करें",
    },
}


async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if source_lang == target_lang:
        return text
    # Mock: In production, call Bhashini API
    # POST https://dhruva-api.bhashini.gov.in/services/inference/pipeline
    # With pipeline config for translation
    return f"[{target_lang.upper()}] {text}"


async def detect_language(text: str) -> str:
    # Mock: In production, use Bhashini LID (Language Identification)
    telugu_chars = any('ఀ' <= c <= '౿' for c in text)
    devanagari_chars = any('ऀ' <= c <= 'ॿ' for c in text)
    if telugu_chars:
        return "te"
    if devanagari_chars:
        return "hi"
    return "en"
