import pyttsx3
import datetime
import pyaudio
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
from plyer import notification
from pygame import mixer
import os
import wolframalpha
import openai
import random
from email.message import EmailMessage
#simplemailtransfer protocol
import smtplib
from newsapi import NewsApiClient


#from decouple import config





EMAIL = "garapatirohanbhaskar@gmail.com"
#PASSWORD = "rohanbhaskar145@gmai"
PASSWORD = ""

NEWS_API_KEY = "57b7ed5969d74b9ba04867ca958a5404"
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

openai.api_key = "sk-proj-MemVUuqBekSrrKUOyYTWT3BlbkFJ2xY590iTuWaNkT6i9YtO"

def get_openai_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text



def send_email(receiver_add,message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
       
        email['From'] = EMAIL
        
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()
        
        return True
    except Exception as e:
        print(e)
        return False

def get_news():
    # Get the top headlines from a specific country
    top_headlines = newsapi.get_top_headlines(country='in')  # You can change the country

    if 'articles' in top_headlines:
        articles = top_headlines['articles']
        news_str = "Here are some of the latest news headlines. "
        # Read the top 5 headlines
        for article in articles[:2]:  # You can adjust the number of headlines to read
            news_str += f"Headline: {article['title']}. "
            news_str += f"{article['description']} "
        return news_str
    else:
        return "I couldn't fetch the news right now. Please try again later."







def say(text):
    os.system(f'say "{text}"')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)




def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    

    
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning")
    elif hour>=12 and hour<18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")
    
    speak("i am Asta sir please tell me how can i help you")
    
def takecommand():
    #it recognises what we tell in microphone and  give string output
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening........")
        #parse threshold is used to continue to listen the text if we take 1 second gap bw the words
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said : {query}\n")
    
    except Exception as e:
        #print(e)
        
        
        print("say that again please")
        return "None"
    return query
       
if __name__ == "__main__":
    wishme()
     
    while True:
    
     query = takecommand().lower()
        
     if 'wikipedia' in query:
          speak('searching in wikipedia...')
          query = query.replace("wikipedia", "")
          results = wikipedia.summary(query, sentences=2)
          speak("According to wikipedia")
          print(results)
          speak(results)
          TimeoutError=None
          
     elif 'open youtube' in query:
         webbrowser.open("youtube.com")
         
     elif 'open google' in query:
         webbrowser.open('google.com') 
         
     elif 'exit' in query:
         speak("shutting down sir have a nice day")
         exit()
         
        
     elif 'remember that' in query:
         rememberMessage = query.replace('remember that',"")
         #rememberMessage = query.replace('Asta',"")
         speak("you told me to remember that" + rememberMessage)
         remember = open("Remember.txt","a")
         remember.write(rememberMessage)
         remember.close()
         
         
     elif 'what do you remember' in query:
         remember = open("Remember.txt","r")
         speak("you told me to remember that" + remember.read())
         
     elif 'schedule my day' in query:
            speak("Preparing your schedule")
            tasks = []
            no_tasks = int(input("Enter total tasks: "))
            with open("tasks.txt", "w") as file:
                for i in range(no_tasks):
                    task = input(f"Enter your task {i + 1}: ")
                    tasks.append(task)
                    file.write(f"{i + 1}. {task}\n")
         
     elif "show my schedule" in query:
            # Play a notification sound
            mixer.init()  # initialize mixer
            mixer.music.load("notification.mp3")
            mixer.music.play()  # play the notification sound

            # Read the schedule from the file and create a pop-up notification
            with open("tasks.txt", "r") as file:
                schedule_content = file.read()

            # Create a desktop notification
            notification.notify(
                title="My Schedule",
                message=schedule_content,
                timeout=15,  # Display notification for 15 seconds
            )
     
     
                 
     
        
     elif "Using artificial intelligence" in query:
         ai(prompt=query)
         
     elif "calculate" in query:
         app_id = "4RQ2T6-U2A42KY3G2"
         client = wolframalpha.Client(app_id)
         ind = query.lower().split().index("calculate")  
         text = query.split()[ind + 1:]
         result = client.query(" ".join(text)) 
         try:
             ans = next(result.results).text
             speak("the anser is: " + ans)
             print("the answer is: "+ ans)
         except StopIteration:
             speak("i coudn't find that.please try again")
             
        
     elif "what is" in query or "who is" in query or "which is" in query:
          app_id = "4RQ2T6-U2A42KY3G2"
          client = wolframalpha.Client(app_id)
          try:
              ind= query.lower().index('what is') if 'what is' in query.lower() else \
                  query.lower().index('who is') if 'who is' in query.lower() else \
                  query.lower().index('which is') if 'which is' in query.lower() else None
                  
              if ind is not None:
                  text = query.split()[ind+2:]
                  result = client.query(" ".join(text))
                  ans = next(result.results).text  
                  speak("the answer is: " + ans)
                  print("the answer is: " + ans)
                  
              else:
                  speak("i couldn't not find that")
                  
          except StopIteration:
              speak("i couldn't find that.please try again")
              
     elif "send an email" in query:
         speak("enter email on terminal sir: ")
         receiver_add = input("Email address:")
         speak("what is the message")
         message = takecommand().capitalize()
         if send_email(receiver_add,message):
             speak("i have sent the email sir")
             print("i have sent the email sir")
         else:
                speak("something went wrong")    
                
     elif "who are you" in query:
         speak("iam Asta  advanced voice assistant")    
         print("iam Asta  advanced voice assistant version 2.0")  
         
     elif "who made you" in query:
         speak("i was made by professor rohan in the laboratory")
         
     elif "read headlines" in query:
            speak(f"i am reading out the headlines of today")
            speak(get_news()) 
            speak("i am printing the headlines on screen")
            print(get_news(),sep='\n')
            # Speak the latest news
            
            
     elif "tell me date and time" in query:
            current_time = datetime.datetime.now()
            date_time_str = current_time.strftime("Today is %A, %B %d, %Y, and the time is %I:%M %p")
            speak(date_time_str)
            print(date_time_str)
            
     elif "mark" in query:
            prompt = query.replace("openai", "").strip()
            if prompt:
                response = get_openai_response(prompt)
                print(f"OpenAI response: {response}")
                speak(f"OpenAI response: {response}")
            else:
                speak("I need a prompt to process with OpenAI.")