import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
import musicLibrary

# ===== CONFIG =====
NEWS_API_KEY = "47e733f35655427bb37cca9665823618"
# OPENAI_API_KEY = "<Your OpenAI API Key Here>"
WAKE_WORD = "jarvis"

# ===== INIT =====
recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()


# ===== SPEAK FUNCTIONS =====
def speak_old(text):
    """Offline speech (robotic but fast)"""
    engine.say(text)
    engine.runAndWait()


def speak(text):
    """Google TTS (natural voice)"""
    try:
        tts = gTTS(text)
        tts.save("temp.mp3")
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait until done
            pass
        pygame.mixer.music.unload()  # Release file before deletion
        os.remove("temp.mp3")
    except Exception as e:
        print(f"TTS error: {e}")
        speak_old(text)  # fallback to pyttsx3


# ===== AI PROCESSING =====
def ai_process(command):
    # """Send the command to OpenAI and return the response"""
    #     client = OpenAI(api_key=OPENAI_API_KEY)
    #     completion = client.chat.completions.create(
    #         model="gpt-3.5-turbo",  # You can change this to gpt-4 if available
    #         messages=[
    #             {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant. Give short and clear responses."},
    #             {"role": "user", "content": command},
    #         ],
    #     )
    #     return completion.choices[0].message.content

    """Process command using local AI server(Ollama3)"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": command, "stream": False},
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "I couldn't think of anything.")
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Local AI error: {e}"


# ===== COMMAND HANDLER =====
def process_command(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif c.startswith("play "):
        song = c.replace("play ", "").strip().lower()
        music_lower = {k.lower(): v for k, v in musicLibrary.music.items()}
        if song in music_lower:
            webbrowser.open(music_lower[song])
            speak(f"Playing {song}")
        else:
            speak("Sorry, I don't know that song.")

    elif "news" in c:
        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
            )
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                if articles:
                    speak("Here are the top headlines.")
                    for article in articles[:5]:
                        speak(article["title"])
                else:
                    speak("No news found.")
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            speak(f"Error fetching news: {e}")

    else:
        output = ai_process(c)
        speak(output)


# ===== MAIN LOOP =====
if __name__ == "__main__":
    speak("Initializing Jarvis... Say 'Jarvis' to wake me up.")

    while True:
        try:
            # Listening for wake word
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            try:
                word = recognizer.recognize_google(audio)
                print(f"You said: {word}")
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Speech Recognition service unavailable.")
                continue

            if WAKE_WORD in word.lower():
                speak("Yes, I'm listening.")
                # Conversation mode
                while True:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        print("Listening for your command...")
                        try:
                            audio = recognizer.listen(
                                source, timeout=8, phrase_time_limit=8
                            )
                            command = recognizer.recognize_google(audio)
                            print(f"Command: {command}")
                        except sr.WaitTimeoutError:
                            speak("I didn't hear anything. Please try again.")
                            continue
                        except sr.UnknownValueError:
                            speak("Sorry, I didn't catch that.")
                            continue
                        except sr.RequestError:
                            speak("Speech recognition service is not available.")
                            break

                        if any(
                            phrase in command.lower()
                            for phrase in ["stop listening", "goodbye", "exit"]
                        ):
                            speak("Okay, going back to standby.")
                            break

                        process_command(command)

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye!")
            break
