import datetime
from datetime import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 
import speech_recognition as sr
import json
import pickle
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import random
number = random.randint(1, 10)
print("Random number:", number)
import numpy as np
import psutil 
import subprocess
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query, 
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = datetime.now().hour
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning khushi, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon khushi, it's {day} and the time is {t}")
    else:
        speak(f"Good evening khushi, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "Boss, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "Boss, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "Boss, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "phone" in command:
        speak("opening dialer")
        os.startfile('"C:\Windows\System32\dialer.exe"')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        try:
            subprocess.run(["taskkill", "/f", "/im", "CalculatorApp.exe"], check=True)
            print("Calculator closed.")
        except subprocess.CalledProcessError:
            print("Calculator is not running.")
    elif "notepad" in command:
        speak("closing notepad")
        try:
            subprocess.run(["taskkill", "/f", "/im", "notepad.exe"], check=True)
            print("notepad closed.")
        except subprocess.CalledProcessError:
            print("notepad is not running.")
    elif "phone" in command:
        speak("closing dialer")
        try:
            subprocess.run(["taskkill", "/f", "/im", "dialer.exe"], check=True)
            print("dialer closed.")
        except subprocess.CalledProcessError:
            print("dialer is not running.")

def browsing(query):
    if 'google' in query:
        speak("Boss, what should I search on Google?")
        s = command().lower()  # get the search term from the user
        search_url = f"https://www.google.com/search?q={s}"
        webbrowser.open(search_url)
    elif 'edge' in query:
        speak("Opening Microsoft Edge")
        # Path to Edge browser (default for Windows)
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        os.startfile(edge_path)

def screenshot():
    filename = f"screenshot_{datetime.now():%d}.png"
    pyautogui.screenshot(filename)
    speak(f"Screenshot saved as {filename}")

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage >= 80:
        speak("Boss, we're fully powered up! Plenty of juice to keep the show running smoothly.")
    elif 40 <= percentage <= 75:
      speak("Boss, we're doing okay, but it's a good time to plug in the charger to stay safe.")
    elif 20 <= percentage < 40:
        speak("Boss, we're running low on power. I recommend connecting the charger soon.")
    else:
        speak("Warning, Boss! We're critically low on battery. Please plug in the charger immediately or the system might shut down.")

def scenario(command):
    if 'leetcode' in command:
        speak("opening leetcode")
        webbrowser.open("https://leetcode.com/")
    elif 'github' in command:
        speak("opening github")
        webbrowser.open("https://github.com/")
    elif 'microsoft 365' in command:
        speak("opening microsoft website")
        webbrowser.open("https://m365.cloud.microsoft/?auth=1")
    elif 'gmail' in command:
        speak("opening your gmail account")
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    else:
        speak("No result found")


if __name__ == "__main__":
    wishMe()
    # engine_talk("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    while True:
        query = command().lower()
        #query  = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open phone" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close phone" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:                   
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
                
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif("take screenshot" in query):
            screenshot()
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif("leetcode" in query) or ("gmail" in query) or("microsoft 365" in query) or ("github" in query):
            speak("opening your website")
            scenario(query)
        elif "exit" in query:
            sys.exit()