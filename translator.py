# translator.py
# Translation and text-to-speech logic (no UI code here)

from functools import lru_cache
from io import BytesIO

from deep_translator import GoogleTranslator
from gtts import gTTS


class TranslationError(Exception):
    """Raised when a translation cannot be completed."""


def get_supported_languages():
    """Return {'english': 'en', 'urdu': 'ur', ...} for the dropdown menus."""
    return GoogleTranslator().get_supported_languages(as_dict=True)


@lru_cache(maxsize=256)
def _translate_cached(text, source_language, target_language):
    # Successful results are cached, so repeating the same text sends no new request.
    return GoogleTranslator(
        source=source_language, target=target_language
    ).translate(text)


def translate_text(text, source_language, target_language):
    """Return the translated text, or raise TranslationError."""
    if not text or not text.strip():
        raise TranslationError("Please enter some text to translate.")

    if source_language == target_language:
        raise TranslationError("Source and target languages are the same.")

    try:
        result = _translate_cached(text.strip(), source_language, target_language)
    except Exception as error:
        if "too many requests" in str(error).lower():
            raise TranslationError(
                "Google Translate is limiting requests right now. "
                "Please wait a minute and try again."
            ) from error
        raise TranslationError(f"Translation failed: {error}") from error

    if not result:
        raise TranslationError("No translation was returned. Try different text.")

    return result


def text_to_speech(text, language_code):
    """Return MP3 audio as bytes, or None if audio is unavailable."""
    if not text or not text.strip():
        return None

    try:
        buffer = BytesIO()
        gTTS(text=text, lang=language_code, slow=False).write_to_fp(buffer)
        return buffer.getvalue()
    except Exception as error:
        print(f"Text-to-speech error: {error}")
        return None


if __name__ == "__main__":
    # Quick manual check: python translator.py
    print(translate_text("Hello, how are you?", "en", "ur"))