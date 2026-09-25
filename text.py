import speech_recognition as sr
import pyttsx3
import datetime

def take_note():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎙️ Speak now...")
        recognizer.adjust_for_ambient_nosie(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("📝 Note captured:", text)

        #Save to Markdown file
        filename = f"note_{datetime.date.today()}.md"
        with open(filename, "a") as f:
            f.write(f"- {datetime.date.now().strftime('%H:%M:%S')}: {text}\n")
        print(f"✅ Saved to {filename}")

        #Optional: read back
        engine = pytssx3.init()
        engine.say("Your note has been saved.")
        engine.runAndWait()

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError:
        print("⚠️ Speech recognition service unavailable")

# Example usage
take_note()