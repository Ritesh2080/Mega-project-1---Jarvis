# Jarvis - Ai assistant
# Can open websites like youtube, google,facebook
# Can give ai responses to query
# Can play the music


import os
import webbrowser as wb

import google.generativeai as genai
import pyttsx3
import requests
import speech_recognition as sr

import musicLibrary

api_key = os.environ.get("api_key")
newsApi = os.environ.get("newsapi")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def speak(word):

    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()


def processCommand(command):
    if "open youtube" in command.lower():
        wb.open("https://www.youtube.com/")

    elif "open google" in command.lower():
        wb.open("https://www.google.com/")

    elif "open facebook" in command.lower():
        wb.open("https://www.facebook.com/")

    elif "open linkedin" in command.lower():
        wb.open("https://www.linkedin.com/")

    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.song[song]
        wb.open(link)

    elif "news" in command.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsApi}"
        )
        print(r.json())
        data = r.json()
        if data["status"] == "ok":
            articles = data.get("articles", [])
            for article in articles:
                speak(article["title"])
    else:
        output = ai_process(command)
        speak(output)


def ai_process(command):
    response = model.generate_content(command)
    print(response.text)
    text = response.text.split(".")[0]
    return text


if __name__ == "__main__":
    speak("Intializing Jarvis!")
    speak("You can tell me do things by calling my name")
    while True:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Recongnizing...")
                audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio)
            if command.lower() == "jarvis":

                while True:
                    try:
                        with sr.Microphone() as source:
                            speak("Ya")
                            print("Jarvis Active...")
                            audio = r.listen(source, timeout=5)
                        command = r.recognize_google(audio)
                        processCommand(command)
                        print(command)
                        break
                    except Exception as e:
                        print(e)
                        speak("did not get the command")
                        speak("going to sleep")
                        break

            if command.lower() == "exit":
                break

        except Exception as e:
            print(e)
