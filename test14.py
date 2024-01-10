import speech_recognition as sr
import pyttsx3
import cv2
import datetime
import spotipy
import os
import webbrowser
import time
import smtplib
import wikipedia
import wolframalpha
import subprocess
import requests
import random
import urllib.parse
from gtts import gTTS
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, jsonify, session
# app = Flask(__name__)

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = 'fc25b57fccf84cdf873b44cfab52da23'
SPOTIPY_CLIENT_SECRET = '2b800627e23149dc82152e26595d580a'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

# Set up Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-playback-state,user-modify-playback-state'))


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/search/<query>')
# def search(query):
#     results = sp.search(q=query, type='track', limit=10)
#     return jsonify(results)

# @app.route('/login')
# def login():
#     scope = 'user-read-private user-read-email'

#     params = {
#         'client_id': SPOTIPY_CLIENT_ID,
#         'response_type': 'code',
#         'scope': scope,
#         'redirect_uri': SPOTIPY_REDIRECT_URI,
#         'show_dialog': True
#     }

#     auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

#     return redirect(auth_url)

# @app.route('/callback')
# def callback():
#     if 'error' in request.args:
#         return jsonify({"error": request.args['error']})
    
#     if 'code' in request.args:
#         req_body = {
#             'code': request.args['code'],
#             'grant_type': 'authorization_code',
#             'redirect_uri': SPOTIPY_REDIRECT_URI,
#             'client_id': SPOTIPY_CLIENT_ID,
#             'client_secret': SPOTIPY_CLIENT_SECRET
#         }

#         response = requests.post(TOKEN_URL, data=req_body)
#         token_info = response.json()

#         session['access_token'] = token_info['access_token']
#         session['refresh_token'] = token_info['refresh_token']
#         session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']

#         return redirect('/playlists')

# @app.route('/playlists')
# def get_playlists():
#     if 'access_token' not in session:
#         return redirect('/login')
    
#     if datetime.datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh-token')

#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }

#     response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
#     playlists = response.json()

#     return jsonify(playlists)

# @app.route('/refresh-token')
# def refresh_token():
#     if 'refresh_token' not in session:
#         return redirect('/login')
    
#     if datetime.datetime.now().timestamp() > session['expires_at']:
#         req_body = {
#             'grant_type': 'refresh_token',
#             'refresh_token': session['refresh_token'],
#             'client_id': SPOTIPY_CLIENT_ID,
#             'client_secret': SPOTIPY_CLIENT_SECRET
#         }

#         response = requests.post(TOKEN_URL, data=req_body)
#         new_token_info = response.json()

#         session['access_token'] = new_token_info['access_token']
#         session['expires_at'] = datetime.datetime.now().timestamp() + new_token_info['expires_in']

#         return redirect('/playlists')

# if __name__ == '__main__':
#     app.run(debug=True)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def greet():
    responses = [
        "Hello, I am Gryzen A I. How can I assist you today?",
        "Hi there! Gryzen A I is ready to help.",
        "Greetings! I'm Gryzen A I. What can I do for you?",
        "Hello! How can I assist you today?"
    ]
    speak(random.choice(responses))

def greet():
    speak("Hello, I am Gryzen A I")

def get_user_name():
    speak("May I know your name?")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        name = recognizer.recognize_google(audio)
        return name
    except sr.UnknownValueError:
        speak("I couldn't understand your name. Please try again.")
        return get_user_name()
    except sr.RequestError:
        speak("Sorry, I'm having trouble with my speech recognition service.")
        return None

def sendEmail(to, content):
    print("Sending mail to ", to)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # paste your email id and password in the respective places
    server.login('Shubhamsisodiya182@gmail.com', 'Shubham@7373')
    server.sendmail('shubhamsisodiya182@gmail.com', to, content)
    server.close()

def getWeather(city_name):
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"  # base url from where we extract weather report
    url = baseUrl + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name
    response = requests.get(url)
    x = response.json()
    # If there is no error, getting all the weather conditions
    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"]
        temp -= 273
        pressure = y["pressure"]
        humidity = y["humidity"]
        desc = x["weather"]
        description = desc[0]["description"]
        info = (" Temperature= " + str(temp) + "°C" + "\n atmospheric pressure (hPa) =" + str(
            pressure) + "\n humidity = " + str(humidity) + "%" + "\n description = " + str(description))
        print(info)
        speak("Here is the weather report at")
        speak(city_name)
        speak(info)
    else:
        speak(" City Not Found ")
def play_song(track_name, artist_name=None, device_id=None):
    try:
        # Search for the track
        if artist_name:
            query = f'track:{track_name} artist:{artist_name}'
        else:
            query = f'track:{track_name}'

        results = sp.search(q=query, type='track', limit=1)

        # Check if there are any results
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']

            # Play the track on the specified device
            response = sp.start_playback(uris=[track_uri], device_id=device_id)
            print("Spotify API Response:", response)

            print(f"Now playing: {track_name} by {artist_name or 'Unknown'} on device {device_id}")
        else:
            print(f"Track not found: {track_name} by {artist_name or 'Unknown'}")
    except spotipy.SpotifyException as e:
        print(f"Error: {e}")




def take_photo(photo_path):

    # Open default camera (usually laptop webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        speak("Error: Unable to access the camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Generate a unique filename based on current date and time
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{current_time}.png"

    # Save the captured frame as an image
    photo_full_path = os.path.join(photo_path, filename)
    cv2.imwrite(photo_full_path, frame)

    # Release the camera
    cap.release()

    # Inform the user
    speak(f"Photo taken and saved as {filename}")
    
    
def getNews():
    try:
        response = requests.get('https://www.bbc.com/news')

        b4soup = BeautifulSoup(response.text, 'html.parser')
        headLines = b4soup.find('body').find_all('h3')
        unwantedLines = ['BBC World News TV', 'BBC World Service Radio',
                         'News daily newsletter', 'Mobile app', 'Get in touch']
        for x in list(dict.fromkeys(headLines)):
            if x.text.strip() not in unwantedLines:
                print(x.text.strip())
    except Exception as e:
        print(str(e))


def process_command(command):
    if "weather" in command:
        speak("Please tell your city name.")
        city_name = input("City name: ")  # Get user input for the city name
        getWeather(city_name)

        command = "weather"
        process_command(command)

    elif "send email" in command:
        try:
            speak("Whom should I send the mail")
            to = input()
            speak("What is the body?")
            content = command()
            sendEmail(to, content)
            speak("Email has been sent successfully !")
        except Exception as e:
            print(e)
            speak("I am sorry, not able to send this email")
    elif "search" in command:
        speak("What would you like to search for?")
        search_query = listen_for_command()
        speak(f"Searching the web for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "open YouTube" in command:
        speak("Opening YouTube...")
        webbrowser.open_new("https://www.youtube.com")
    elif "exit" in command:
        speak("Goodbye! Have a great day.")
        exit()
    elif 'log off' in command or 'sign out' in command:
        speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
        time.sleep(10)
        subprocess.call(["shutdown", "/l"])
    else:
        # Additional features from the given script
        if 'wikipedia' in command:
            speak('Searching Wikipedia')
            command = command.replace("wikipedia", "")
            results = wikipedia.summary(command, sentences = 3)
            speak("These are the results from Wikipedia")
            print(results)
            speak(results)
        elif 'ask' in command:
            speak('I can answer computational and geographical questions. What question do you want to ask now?')
            question = listen_for_command()
            app_id = "your_wolfram_alpha_app_id"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        
        elif 'news' in command:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India. Happy reading.')
            time.sleep(6)
        elif 'camera' in command or 'take a photo' in command:
         take_photo(photo_path="C:/Users/Shubham/Downloads/music")  
         # Update the path accordingly
         speak('Photo taken!')
        elif 'play song' in command:
            speak("Sure! Please tell me the name of the song and the artist.")
            song_and_artist = listen_for_command()

            try:
                song_name, artist_name = song_and_artist.split(" by ")
            except ValueError:
                song_name = song_and_artist
                artist_name = None

            # Obtain the device ID by checking Spotify devices
            devices = sp.devices()
            if devices['devices']:
                device_id = devices['devices'][0]['id']  # Use the first available device ID
                play_song(song_name, artist_name, device_id)
            else:
                print("No active devices found.")
            print("Command processing complete")


        elif 'who are you' in command or 'what can you do' in command:
            speak(
                'I am Gryzen A I, your personal AI assistant. I can perform various tasks like opening YouTube, Google Chrome, Gmail, and more. '
                'You can ask me to take a photo, search Wikipedia, predict the weather, and much more!')
        elif 'who made you' in command or 'who created you' in command:
            speak("I was built by F_NAME")
            print("I was built by F_NAME")
        elif 'shutdown system' in command:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')
        elif "restart" in command:
            subprocess.call(["shutdown", "/r"])
        elif "sleep" in command:
            speak("Setting in sleep mode")
            subprocess.call("shutdown / h")
        elif "write a note" in command:
            speak("What should i write, sir")
            note = write_note()
            file = open('Grysen A I.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = write_note()

def credits():
    speak("I am Gryzen A I, your personal AI assistant. I can perform various tasks like opening Gmail, Google Chrome, YouTube, fetching data from Wikipedia, predicting the time, taking photos, fetching the latest news, searching the web, answering computational questions using Wolfram Alpha, and weather forecasting. I was created by F_NAME.")


def get_voice_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            print("Speak now...")
            audio = recognizer.listen(source, timeout=5)
            print("Listening done.")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("UnknownValueError: Sorry, I couldn't understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"RequestError: Error with the speech recognition service; {e}")
            return None

def write_note():
    note_content = get_voice_input()

    if note_content:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        note = f"{current_time}\n{note_content}"

        file_path = "notes.txt"
        with open(file_path, "a") as file:
            file.write(note + "\n\n")

        print("Note written successfully!")

        tts = gTTS(text=note_content, lang='en')
        tts.save("note.mp3")
        os.system("start note.mp3")
    else:
        print("Unable to get voice input. Note not written.")

def extract_name(command):
    # Check if the command contains "my name is"
    if "my name is" in command.lower():
        # Extract the name following "my name is"
        name_index = command.lower().index("my name is") + len("my name is")
        name = command[name_index:].strip()
        return name
    else:
        # If "my name is" is not present, return the full command
        return command


def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=5)
            print("Listening done.")
            command = recognizer.recognize_google(audio)
            print("User Command:", command)
            return command
        except sr.UnknownValueError:
            print("UnknownValueError: I couldn't understand the audio. Listening again...")
            speak("I couldn't understand your command. Please try again.")
            return listen_for_command()
        except sr.RequestError as e:
            print(f"RequestError: {e}")
            speak("Sorry, I'm having trouble with my speech recognition service.")
            return None



if __name__ == "__main__":
    greet()
    user_name = get_user_name()
    if user_name:
        speak(f"Nice to meet you, {user_name}!")
        while True:
            speak("How can I assist you?")
            command = listen_for_command()
            process_command(command)
