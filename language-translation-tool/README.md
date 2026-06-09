# 🌐 AI Language Translation Tool

A professional AI-powered language translation web application built 
with Python and Streamlit. Translates text between 100+ languages 
instantly using Google Translate AI.

---

## 🖼️ Features

- 🔁 Translate between 100+ languages instantly
- 🔍 Auto-detect source language
- 🔊 Text-to-speech audio playback
- 📋 One-click copy translated text
- 🎨 Beautiful dark-themed UI
- ⚡ Fast and responsive interface

---

## 🛠️ Tech Stack

| Technology     | Purpose                        |
|----------------|-------------------------------|
| Python 3.x     | Core programming language      |
| Streamlit      | Web UI framework               |
| deep-translator| Google Translate API wrapper   |
| gTTS           | Google Text-to-Speech          |
| Git & GitHub   | Version control & hosting      |

---

## 📁 Project Structure
translation-tool/
│
├── app.py              # Streamlit UI — the face of the app
├── translator.py       # Translation logic — the brain
├── requirements.txt    # All required Python libraries
├── README.md           # Project documentation
└── .gitignore          # Files excluded from Git

---

## ⚙️ How to Run Locally

### Step 1 — Clone the repository
git clone https://github.com/ash-1212/translation-tool.git
cd translation-tool

### Step 2 — Create virtual environment
python -m venv venv
venv\Scripts\activate

### Step 3 — Install dependencies
pip install -r requirements.txt

### Step 4 — Run the app
streamlit run app.py

### Step 5 — Open in browser
http://localhost:8501

---

## 🔄 How It Works
User types text + selects languages
↓
Streamlit UI captures input
↓
translator.py sends to Google Translate
↓
Translated text returned
↓
Result displayed + audio generated

---

## 📸 App Preview

> Dark themed professional UI with language selector,
> text input, instant translation, and audio playback.

---

## 👨‍💻 Author

- **Name:** Ayesha Nazish
- **Internship:** CodeAlpha AI Internship


---

## 📄 License

This project is open source and available under the MIT License.

