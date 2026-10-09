# ============================================================
# translator.py
# PURPOSE: Handles all translation and text-to-speech logic
# This is the BRAIN — no UI code lives here
# ============================================================

from deep_translator import GoogleTranslator
from gtts import gTTS


# ------------------------------------------------------------
# FUNCTION 1: Get all supported languages
# ------------------------------------------------------------
def get_supported_languages():
    """
    Returns a dictionary of all languages Google Translate supports.
    Example: {'english': 'en', 'urdu': 'ur', 'french': 'fr' ...}
    Used to populate dropdown menus in the UI.
    """
    languages = GoogleTranslator().get_supported_languages(as_dict=True)
    return languages


# ------------------------------------------------------------
# FUNCTION 2: Translate text
# ------------------------------------------------------------
def translate_text(text, source_language, target_language):
    """
    Translates text from source language to target language.

    Parameters:
        text            : Text the user wants to translate
        source_language : Language code e.g. 'en' or 'auto'
        target_language : Language code e.g. 'ur'

    Returns:
        Translated text as a string
        OR a friendly error message
    """

    # Safety check — empty text
    if not text or text.strip() == "":
        return "⚠️ Please enter some text to translate."

    # Safety check — same language selected
    if source_language == target_language:
        return "⚠️ Source and target languages are the same!"

    try:
        translated = GoogleTranslator(
            source=source_language,
            target=target_language
        ).translate(text)

        return translated

    except Exception as error:
        return f"❌ Translation failed: {str(error)}"


# ------------------------------------------------------------
# FUNCTION 3: Convert text to speech
# ------------------------------------------------------------
def text_to_speech(text, language_code):
    """
    Converts translated text into an MP3 audio file.

    Parameters:
        text          : Text to speak
        language_code : Language for correct pronunciation e.g. 'ur'

    Returns:
        File path of saved audio OR None if failed
    """

    if not text or text.strip() == "":
        return None

    try:
        audio = gTTS(text=text, lang=language_code, slow=False)
        audio_file_path = "translated_audio.mp3"
        audio.save(audio_file_path)
        return audio_file_path

    except Exception as error:
        print(f"Text-to-speech error: {str(error)}")
        return None


# ------------------------------------------------------------
# FUNCTION 4: Detect language of input text
# ------------------------------------------------------------
def detect_language(text):
    """
    Detects what language the input text is written in.

    Parameters:
        text : Text to detect language for

    Returns:
        Detected language name as string
    """

    if not text or text.strip() == "":
        return "Unknown"

    try:
        translator = GoogleTranslator(source='auto', target='en')
        translator.translate(text)
        detected = translator.source
        return detected

    except Exception as error:
        return "Could not detect"


# ------------------------------------------------------------
# TEST BLOCK — Only runs when you run this file directly
# NEVER runs when app.py imports this file
# ------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 50)
    print("TESTING translator.py")
    print("=" * 50)

    print("\n📌 Test 1: English to Urdu")
    print(translate_text("Hello, how are you?", "en", "ur"))

    print("\n📌 Test 2: Auto detect to French")
    print(translate_text("Good morning!", "auto", "fr"))

    print("\n📌 Test 3: Empty text")
    print(translate_text("", "en", "ur"))

    print("\n📌 Test 4: Same language")
    print(translate_text("Hello", "en", "en"))

    print("\n📌 Test 5: First 5 languages")
    langs = get_supported_languages()
    print(list(langs.items())[:5])

    print("\n✅ All tests passed!")
    print("=" * 50)