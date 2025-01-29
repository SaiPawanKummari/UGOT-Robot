import time
from datetime import datetime
import requests
from ugot import ugot

# Initialize Ugot bot
bot = ugot.UGOT()
bot.initialize('192.168.0.128')  # Replace with your robot's IP address

# Configuration
ACTIVATION_PHRASE = "hi robot"
ROBOT_GREETING = "Hi! What's up?"
VOICE_TYPE = 0  # 0: female, 1: male
WEATHER_API_KEY = "cced7304cf2d9682853bbb65887b8de1"  # OpenWeatherMap API key
WEATHER_LOCATION = "India"  # Replace with your desired location

# Utility Functions
def get_current_time():
    """Returns the current time in a human-readable format."""
    return datetime.now().strftime("%I:%M %p")

def get_current_date():
    """Returns the current date in a human-readable format."""
    return datetime.now().strftime("%A, %d %B %Y")

def get_weather():
    """Fetches weather information using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_LOCATION}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            return f"The current temperature in {WEATHER_LOCATION} is {temp} degrees Celsius with {weather_desc}."
        else:
            return "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        return "There was an error retrieving the weather data."

# Infinite Loop to Process User Inputs
while True:
    try:
        audio = bot.start_audio_asr()  # Start mic and get user input
        if audio.lower().find(ACTIVATION_PHRASE.lower()) != -1:  # Check activation
            bot.play_audio_tts(ROBOT_GREETING, wait=True, voice_type=VOICE_TYPE)
            time.sleep(0.5)  # Allow greeting to complete

            while True:
                query = bot.start_audio_asr().strip()  # Get user query

                # Handle queries
                if "time" in query.lower():
                    response = f"The current time is {get_current_time()}."
                elif "date" in query.lower():
                    response = f"Today's date is {get_current_date()}."
                elif "weather" in query.lower():
                    response = get_weather()
                elif query.lower() in ["exit", "stop", "shutdown"]:
                    response = "Goodbye! Shutting down."
                    bot.play_audio_tts(response, wait=True, voice_type=VOICE_TYPE)
                    print("Exiting program...")
                    exit(0)
                else:
                    # Fallback to AI NLP for other queries
                    response = bot.start_audio_nlp(query, wait=True)

                # Speak response
                bot.play_audio_tts(response, wait=True, voice_type=VOICE_TYPE)
                time.sleep(0.5)  # Allow processing time

    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
        bot.play_audio_tts("Goodbye baby! Shutting down.", wait=True, voice_type=VOICE_TYPE)
        break
    except Exception as e:
        print(f"Error: {e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Error: {e}\n")
        bot.play_audio_tts("An error occurred. Check logs for details.", wait=True, voice_type=VOICE_TYPE)
