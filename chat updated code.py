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
                elif "team" in query.lower():
                    response = f"I was assigned to the team consisting of members Mojesh,Sai Pawan,Bharathi and Naveen.And I am glad to be their team."
                elif "Siva Ram" in query.lower():
                    response = f"Dotor.M. Siva Ram Garu is the Managing director of Rajeev gandhi memorial college.He is a young, result driven, self-motivated and resourceful managing director with a proven ability and in charge to lead, develop, motivate and strengthen managing team in the Institution."
                elif "mojesh" in query.lower():
                    response = f"He is a very sweet friend of mine.He is the one who programmed me. He is a student in CSE AIML. He was born on 20 April,2005. And his friends are Sai Pawan,Naveen and Bharathi.  "
                elif "kishore" in query.lower():
                    response = f"Dotor. G. Kishor Kumar sir is the Head of the department of CSE Artificial Intelligence and Machine Learning. He was born on 15 april,1980. He has received Research Excellence Award and Bharat Vikas Award in the year 2017. "
                elif "rgm" in query.lower():
                    response = f"Rajeev Gandhi Memorial College of Engineering and Technology was founded in the year 1995. It is located in a 32.04 acre sprawling campus on NH-40 (old NH-18) at Nandyal, , Andhra Pradesh. It is the dedicated commitment and efforts of our Chairman, the man with vision Vidyarathna Dr. M. Santhiramudu, who started the institution with a motto EDUCATION FOR PEACE. RGMCET is a road of elegant educational journey, yet path breaking in different dimensions."
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
