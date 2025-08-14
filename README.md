# 🎙️ Jarvis - AI Voice Assistant
Jarvis is a Python-based AI voice assistant capable of recognizing voice commands, playing music, opening websites, fetching news, and interacting with a local AI model (LLaMA3) or OpenAI's API for conversational responses.  
It supports both **offline** (PyTTSx3) and **natural voice** (Google TTS) speech synthesis.

---

## ✨ Features
- 🎤 **Voice Activation** using the wake word `"Jarvis"`.
- 🌐 **Web Navigation** — Open Google, YouTube, Facebook, etc.
- 🎵 **Music Playback** — Play songs from a custom music library.
- 📰 **News Fetching** — Get top headlines via NewsAPI.
- 🤖 **AI Chat** — Uses a local LLaMA3 server (or OpenAI API if enabled).
- 🔊 **Dual Speech Output** — Google TTS (natural) or PyTTSx3 (offline).
- 🛑 **Stop Commands** — "stop listening", "goodbye", or "exit" to return to standby.

---

## 📦 Requirements
Install dependencies from the provided `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

## ⚙️ Setup

- Clone the repository
  ```
  git clone https://github.com/harshikab2112/Jarvis-Virtual-Assistant
  cd Jarvis-Virtual-Assistant
  ```

- Install dependencies
  ```
  pip install -r requirements.txt
  ```

- Add API Keys
  - Get a free News API key from https://newsapi.org.
  - Replace the value of NEWS_API_KEY in main.py.
  - (Optional) If using OpenAI, uncomment the relevant code and set OPENAI_API_KEY.
- Add Music Links
  - Edit musicLibrary.py and update song names + YouTube URLs.
 
## ▶️ Usage
Run the assistant:
```
python main.py
```
- Say "Jarvis" to activate.
- Try commands like:
  - Open Google
  - Open YouTube
  - Play Ribs
  - News
  - Tell me a joke

## 📁 Project Structure
```
jarvis-assistant/
│-- main.py             # Main script for Jarvis
│-- musicLibrary.py     # Music dictionary (name: URL)
│-- client.py           # Client script to interact with Jarvis
│-- requirements.txt    # Python dependencies
│-- README.md           # Project documentation
```

## 🛠️ Technologies Used
- SpeechRecognition — For capturing voice commands
- PyTTSx3 & gTTS — For speech output
- pygame — For audio playback
- webbrowser — To open websites
- Requests — To fetch data from APIs
- LLaMA3 / OpenAI API — For AI responses

### 📜 License

This project is open-source. You can modify and use it for personal or educational purposes.

### 🚀 Future Improvements

- Integrate weather updates.
- Add reminder and timer features.
- Improve hotword detection accuracy.
