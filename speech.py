import speech_recognition as sr
import os

recognizer = sr.Recognizer()

def save_to_file(text):
    with open("recognized_speech.txt", "a") as file:
        file.write(text + "\n")

while True:
    try:
        with sr.Microphone() as source:
            print("Say Something....")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = recognizer.recognize_google(audio).lower()
            print(f"Recognized speech: {text}")
            save_to_file(text)
    except sr.UnknownValueError:
        print("Could not understand, please repeat")
    except sr.RequestError:
        print("Could not request results; check your network connection")
    except Exception as e:
        print(f"Error: {e}")
        break
