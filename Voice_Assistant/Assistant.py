import speech_recognition as sr
import pyttsx3
import requests
import smtplib
import schedule
import threading
import time
import datetime
import json
import wikipedia
from transformers import pipeline

# ========== CONFIG ==========
WEATHER_API_KEY = "your_openweather_api_key"
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
IFTTT_WEBHOOK_KEY = "your_ifttt_webhook_key"

# ========== SPEECH + TTS ==========
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# ========== NLP PIPELINE ==========
qa_pipeline = pipeline("question-answering")

# ========== CORE UTILS ==========
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print(" Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""

# ========== WEATHER ==========
def get_weather():
    speak("Which city?")
    city = listen()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        speak("City not found.")
        return
    temp = response['main']['temp']
    desc = response['weather'][0]['description']
    speak(f"Current temperature in {city} is {temp}°C with {desc}.")

# ========== EMAIL ==========
def send_email():
    speak("Who is the recipient?")
    to_email = listen()
    speak("What should I say?")
    content = listen()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, content)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print(e)

# ========== REMINDERS ==========
def set_reminder():
    speak("What should I remind you about?")
    task = listen()
    speak("In how many seconds should I remind you?")
    try:
        delay = int(listen())
        def reminder():
            speak(f"Reminder: {task}")
        schedule.every(delay).seconds.do(reminder)
        threading.Thread(target=run_schedule, daemon=True).start()
        speak("Reminder set.")
    except:
        speak("I couldn't understand the time.")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# ========== SMART HOME ==========
def control_device():
    speak("Say 'on' to turn on light or 'off' to turn off light.")
    state = listen()
    if state == "on":
        requests.get(f"https://maker.ifttt.com/trigger/light_on/with/key/{IFTTT_WEBHOOK_KEY}")
        speak("Light turned on.")
    elif state == "off":
        requests.get(f"https://maker.ifttt.com/trigger/light_off/with/key/{IFTTT_WEBHOOK_KEY}")
        speak("Light turned off.")
    else:
        speak("Invalid command.")

# ========== GENERAL KNOWLEDGE ==========
import wikipedia
import datetime

def answer_question():
    speak("What do you want to know?")
    question = listen()

    if "time" in question:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "date" in question:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    else:
        try:
            result = wikipedia.summary(question, sentences=2)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("That was a bit broad. Can you be more specific?")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn’t find anything about that.")
        except Exception as e:
            speak("Something went wrong while searching Wikipedia.")


# ========== COMMAND HANDLER ==========
def handle_command(command):
    if "weather" in command:
        get_weather()
    elif "email" in command:
        send_email()
    elif "remind" in command:
        set_reminder()
    elif "light" in command:
        control_device()
    elif "question" in command or "know" in command:
        answer_question()
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I didn't understand. Try again.")

# ========== MAIN LOOP ==========
if __name__ == "__main__":
    speak("Hello, I am your assistant. How can I help you today?")
    while True:
        cmd = listen()
        if cmd:
            handle_command(cmd)
