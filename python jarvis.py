import wikipedia
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 160)  # speed of speech

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source)  # reduce background noise
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(f"You: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please say again.")
        return ""
    except sr.RequestError:
        speak("Speech service unavailable.")
        return ""

def jarvis():
    speak("Hello, I am Jarvis. Ask me anything from Wikipedia. Say 'exit' to quit.")

    while True:
        query = listen().lower()

        if query in ["exit", "quit", "bye"]:
            speak("Goodbye! Shutting down...")
            break

        if query.strip() == "":
            continue

        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except wikipedia.DisambiguationError as e:
            speak("Your question is too broad. Did you mean one of these?")
            print(e.options[:5])
        except Exception:
            speak("Sorry, I couldn't find any information on that.")

if __name__ == "__main__":
    jarvis()
