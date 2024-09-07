import os
import pyautogui
import webbrowser
import pyttsx3
import wolframalpha


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)




def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
dictapp = {"commandprompt":"cmd","paint":"paint","word":"winword","excel":"excel","chrome":"chrome","vscode":"code","powerpoint":"powerpoint"}


def openappweb(query):
    speak("launching sirr")
    if ".com" in query or ".co.in" in query or ".org" in query:
        query = query.replace()