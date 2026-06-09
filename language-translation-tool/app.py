# ============================================================
# app.py
# PURPOSE: Beautiful UI for the Language Translation Tool
# Fixed: session_state keeps translation alive between reruns
# ============================================================

import streamlit as st
from translator import translate_text, get_supported_languages, text_to_speech

# ------------------------------------------------------------
# PAGE CONFIGURATION — Must be first Streamlit command
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

# ------------------------------------------------------------
# CUSTOM CSS — Makes the app look professional and beautiful
# ------------------------------------------------------------
st.markdown("""
<style>
    /* ── Background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* ── Main card container ── */
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }

    /* ── Title styling ── */
    .app-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        padding-top: 1rem;
    }

    /* ── Subtitle ── */
    .app-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.55);
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* ── Section labels ── */
    .section-label {
        color: rgba(255,255,255,0.75);
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* ── Swap arrow ── */
    .swap-arrow {
        text-align: center;
        font-size: 1.6rem;
        color: rgba(255,255,255,0.4);
        padding-top: 1.8rem;
    }

    /* ── Result box ── */
    .result-box {
        background: rgba(96, 165, 250, 0.08);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        color: #e2e8f0;
        font-size: 1.05rem;
        line-height: 1.7;
        min-height: 80px;
        word-break: break-word;
    }

    /* ── Character count ── */
    .char-count {
        text-align: right;
        color: rgba(255,255,255,0.35);
        font-size: 0.78rem;
        margin-top: 0.3rem;
    }

    /* ── Success badge ── */
    .success-badge {
        display: inline-block;
        background: rgba(52, 211, 153, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.4);
        color: #34d399;
        border-radius: 20px;
        padding: 0.2rem 0.9rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    /* ── Copy hint ── */
    .copy-hint {
        color: rgba(255,255,255,0.3);
        font-size: 0.78rem;
        margin-top: 0.5rem;
        text-align: right;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.25);
        font-size: 0.78rem;
        padding: 1.5rem 0 1rem;
    }

    /* ── Streamlit widget tweaks ── */
    div[data-testid="stSelectbox"] > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    div[data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-size: 1rem !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder {
        color: rgba(255,255,255,0.25) !important;
    }

    /* ── Primary button ── */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        padding: 0.6rem 0 !important;
        color: white !important;
        transition: opacity 0.2s !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        opacity: 0.88 !important;
    }

    /* ── Secondary button ── */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        color: rgba(255,255,255,0.8) !important;
        font-weight: 600 !important;
    }

    /* ── Audio player ── */
    audio {
        width: 100%;
        border-radius: 10px;
        margin-top: 0.5rem;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* ── Hide Streamlit default header/footer ── */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# SESSION STATE SETUP
# This runs once and creates our "sticky notepad"
# ------------------------------------------------------------
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "target_code" not in st.session_state:
    st.session_state.target_code = ""

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "show_audio" not in st.session_state:
    st.session_state.show_audio = False


# ------------------------------------------------------------
# LOAD LANGUAGES (cached — only fetches once)
# ------------------------------------------------------------
@st.cache_data
def load_languages():
    languages = get_supported_languages()
    language_names = list(languages.keys())
    return languages, language_names


# ------------------------------------------------------------
# MAIN APP
# ------------------------------------------------------------
def main():

    languages, language_names = load_languages()

    # ── Title ───────────────────────────────────────────────
    st.markdown('<div class="app-title">🌐 AI Translator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Translate instantly across 100+ languages powered by Google AI</div>',
        unsafe_allow_html=True
    )

    # ── Language Selector Card ───────────────────────────────
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🗣 Language Pair</div>', unsafe_allow_html=True)

    col1, col_mid, col2 = st.columns([5, 1, 5])

    with col1:
        source_options = ["auto detect"] + language_names
        source_choice = st.selectbox(
            "From",
            options=source_options,
            index=0,
            label_visibility="collapsed"
        )

    with col_mid:
        st.markdown('<div class="swap-arrow">⇄</div>', unsafe_allow_html=True)

    with col2:
        default_target = language_names.index("urdu") if "urdu" in language_names else 0
        target_choice = st.selectbox(
            "To",
            options=language_names,
            index=default_target,
            label_visibility="collapsed"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Input Card ───────────────────────────────────────────
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">✏️ Your Text</div>', unsafe_allow_html=True)

    input_text = st.text_area(
        "Input",
        placeholder="Type or paste your text here...",
        height=160,
        max_chars=5000,
        label_visibility="collapsed"
    )

    if input_text:
        st.markdown(
            f'<div class="char-count">{len(input_text)} / 5000 characters</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Translate Button ─────────────────────────────────────
    translate_clicked = st.button(
        "🔁  Translate Now",
        type="primary",
        use_container_width=True
    )

    # ── Translation Logic ────────────────────────────────────
    if translate_clicked:

        if not input_text.strip():
            st.warning("⚠️ Please enter some text before translating.")

        else:
            source_code = "auto" if source_choice == "auto detect" else languages[source_choice]
            target_code  = languages[target_choice]

            with st.spinner("Translating..."):
                result = translate_text(input_text, source_code, target_code)

            # ✅ Save to session_state — survives button reruns
            st.session_state.translated_text = result
            st.session_state.target_code     = target_code
            st.session_state.audio_bytes     = None   # reset old audio
            st.session_state.show_audio      = False

    # ── Result Card (shows if we have a translation) ─────────
    if st.session_state.translated_text:

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        st.markdown('<span class="success-badge">✅ Translation Ready</span>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">📋 Result</div>', unsafe_allow_html=True)

        # Show translated text in styled box
        st.markdown(
            f'<div class="result-box">{st.session_state.translated_text}</div>',
            unsafe_allow_html=True
        )

        # Copy hint using st.code (has built-in copy button)
        st.code(st.session_state.translated_text, language=None)
        st.markdown(
            '<div class="copy-hint">⬆ Click the copy icon above to copy translated text</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Audio Section ─────────────────────────────────
        st.markdown('<div class="section-label">🔊 Text to Speech</div>', unsafe_allow_html=True)

        play_clicked = st.button(
            "▶️  Generate & Play Audio",
            type="secondary",
            use_container_width=True
        )

        # When play is clicked — generate audio and save to session_state
        if play_clicked:
            with st.spinner("Generating audio..."):
                audio_path = text_to_speech(
                    text=st.session_state.translated_text,
                    language_code=st.session_state.target_code
                )

            if audio_path:
                # Read audio file as bytes and store in session_state
                with open(audio_path, "rb") as f:
                    st.session_state.audio_bytes = f.read()
                st.session_state.show_audio = True
            else:
                st.error("❌ Audio not available for this language.")

        # Show audio player if audio is ready — persists across reruns
        if st.session_state.show_audio and st.session_state.audio_bytes:
            st.audio(st.session_state.audio_bytes, format="audio/mp3")
            st.success("🎵 Playing translation audio!")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────
    st.markdown(
        '<div class="footer">Built with ❤️ using Python · Streamlit · Google Translate AI'
        '<br>CodeAlpha AI Internship Project</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()