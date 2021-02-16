from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
from googleapiclient.discovery import build
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import time
from twilio.rest import Client

# import schedule
import time
from datetime import datetime


app = Flask(__name__)


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if "hello" in incoming_msg:
        quote = "Hi Avi. How are you?"
        msg.body(quote)
        responded = True

    if "meaning" in incoming_msg:
        word_user = incoming_msg.split("of")
        print(word_user[1])
        word = word_user[1]
        wm(word, msg)
        responded = True

    if "fact" in incoming_msg:
        fact(msg)
        responded = True

    if "song" in incoming_msg:
        word_user = incoming_msg.split("song")
        print(word_user[1])
        word = word_user[1]
        song(word, msg)
        responded = True

    if "radio" in incoming_msg:
        radio(msg)
        responded = True

    if "wake" in incoming_msg:
        word = incoming_msg.split("after")
        str1 = " "
        print(word)
        str1 = word[1]
        str1 = str(str1)
        str2 = str1.rstrip()
        str2 = str1.split(" ")
        wake(str2[1])
        responded = True

    if "google" in incoming_msg:
        word_user = incoming_msg.split("google")
        print(word_user[1])
        word = word_user[1]
        google(word, msg)
        responded = True

    if "weather" in incoming_msg:
        word_user = incoming_msg.split("of")
        word = word_user[1]
        weather(word, msg)
        responded = True

    if "calculate" in incoming_msg:
        word_user = incoming_msg.split(" ")
        word = word_user[1]
        math_cal(word, msg)
        responded = True

    if "meetings" in incoming_msg:
        meeting(msg)
        responded = True

    if "movie" in incoming_msg:
        word_user = incoming_msg.split("of")
        word = word_user[1]
        movie_rate(word, msg)
        responded = True

    if "joke" in incoming_msg:
        joke(msg)
        responded = True

    if "holiday" in incoming_msg:
        word_user = incoming_msg.split(",")
        day = word_user[1]
        month = word_user[2]
        year = word_user[3]
        calendar(day, month, year, msg)
        responded = True

    if "news" in incoming_msg:
        wn(msg)
        responded = True

    if "cat" in incoming_msg:
        msg.media("https://cataas.com/cat")
        responded = True
    if not responded:
        msg.body("I only know about bread and butter, not everything sorry!")

    return str(resp)


def wake(word):
    account_sid = "AC4e023ae1e245bd05a7d6607dcf400e3b"
    auth_token = "e7c3ae40a18bbec3c07f2baf68caa9b2"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="Reminder set!",
        to="whatsapp:+919650754366",
    )
    sec = int(word) * 60
    time.sleep(sec)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="Please wake up",
        to="whatsapp:+919650754366",
    )

    print(message.sid)


def wm(word, msg):
    app_id = "f1598e2f"
    app_key = "085d5449add89be116ab7436791df73d"
    endpoint = "entries"
    language_code = "en-us"
    word_id = word
    url = (
        "https://od-api.oxforddictionaries.com/api/v2/"
        + endpoint
        + "/"
        + language_code
        + "/"
        + word_id.lower()
    )
    try:
        r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
        al = r.json()
        meaning = al["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0][
            "shortDefinitions"
        ]
        msg.body(meaning[0])
        responded = True
    except:
        txt = "Sorry, can't fetch at this moment!"
        msg.body(txt)
        responded = True


def math_cal(word, msg):
    res = eval(word)
    msg.body(str(res))
    responded = True


def joke(msg):
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        res = requests.get(url)
        res = res.json()
        line = res["setup"] + " " + res["punchline"]
        print(line)
        msg.body(line)
        responded = True
    except:
        txt = "Sorry, can't fetch at this moment!"
        msg.body(txt)
        responded = True


def fact(msg):
    url = "http://numbersapi.com/random/trivia"
    try:
        res = requests.get(url)
        print(res.text)
        msg.body(res.text)
        responded = True
    except:
        txt = "Sorry, can't fetch at this moment!"
        msg.body(txt)
        responded = True


def radio(msg):
    link = "https://www.radioindia.net/radio/mirchi98/icecast.audio"
    msg.body(str(link))
    responded = True


def movie_rate(word, msg):
    params = (
        ("t", word),
        ("y", ""),
        ("plot", "short"),
        ("r", "json"),
        ("apikey", "4e15beae"),
    )

    try:
        response = requests.get("http://www.omdbapi.com/", params=params)
        res = response.json()
        print(res["Plot"])
        print(res["Ratings"][0]["Value"])
        print(res["Actors"])
        msg.body(res["Plot"])
        msg.body(res["Ratings"][0]["Value"])
        msg.body(res["Actors"])
        responded = True
    except:
        txt = "Sorry, can't fetch at this moment!"
        msg.body(txt)
        responded = True


def calendar(day, month, year, msg):
    params = (
        ("api_key", "9ad2b336db74422f87dcc70a99f75376"),
        ("country", "IN"),
        ("year", year),
        ("month", month),
        ("day", day),
    )
    try:
        response = requests.get("https://holidays.abstractapi.com/v1/", params=params)
        res = response.json()
        msg.body(res[0]["name"])
        responded = True
    except:
        txt = "Sorry, can't fetch at this moment!"
        msg.body(txt)
        responded = True


def wn(msg):
    params = (
        ("country", "in"),
        ("pageSize", "100"),
        ("apiKey", "dee921718665477983e4d38d2ba1e2c2"),
    )
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines", params=params)
        res = response.json()
        news = res["articles"][0]["content"]
        msg.body(news)
        msg.body(res["articles"][1]["content"])
        msg.body(res["articles"][2]["content"])
        msg.body(res["articles"][3]["content"])
        msg.body(res["articles"][4]["content"])
        responded = True
    except:
        txt = "Sorry, can't fetch news at this moment!"
        msg.body(txt)
        responded = True


def weather(word, msg):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {
        "callback": "test",
        "id": "2172797",
        "units": "metric",
        "mode": "xml%2C html",
        "q": {word},
    }
    headers = {
        "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
        "x-rapidapi-key": "ca5c799ea7msh91e3a2b9f0b4841p1f2177jsna4ffa54a686e",
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        msg.body(response.text)
        responded = True
    except:
        txt = "Sorry, can't find the city or connection timed out!"
        msg.body(txt)
        responded = True


def google(word, msg):
    query = word
    word = word.strip()
    word = word.replace(" ", "+")
    url = "https://www.google.com/search?q=" + word
    for j in search(query, tld="com", num=1, stop=1, pause=1):
        msg.body(j)
    responded = True


def song(word, msg):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer BQDdj2gFhOgZEhEtENRqQ1wLGZhr0qbT2XdkWFItQiUhwIeQOaDrkcgixRGCElvHYSyKd2I0XTiscPTuMryB6nTC42TpSKPt6jsN5jNQxEaIqshqipg1wWKcxvJ0-APYo1svyPprxKchHujxS_tdJgrHMYFTDmSMjVo",
    }

    params = (
        ("q", word),
        ("type", "track"),
        ("market", "IN"),
    )
    try:
        response = requests.get(
            "https://api.spotify.com/v1/search", headers=headers, params=params
        )
        data = json.loads(response.content)
        print(data["tracks"]["items"][0]["external_urls"]["spotify"])
        url = data["tracks"]["items"][0]["external_urls"]["spotify"]
        msg.body(url)
        responded = True
    except:
        txt = "Sorry, can't find this song!"
        msg.body(txt)
        responded = True


def meeting(msg):
    scopes = ["https://www.googleapis.com/auth/calendar"]
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret1.json", scopes=scopes
    )
    credentials = pickle.load(open("token.pkl", "rb"))

    with open("token.pickle", "wb") as token:
        pickle.dump(credentials, token)

    service = build("calendar", "v3", credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
        msg.body("*Meeting*")
        msg.body("\n\n")
        msg.body(start)
        msg.body(event["summary"])


if __name__ == "__main__":
    app.run()
