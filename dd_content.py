import csv
import os
import random
from urllib import request
import json
import datetime
import bbc

from dotenv import load_dotenv

load_dotenv()


def get_random_quote(quotes_file="quotes.csv"):
    """
    Get a random quote from a CSV file
    """
    try:
        with open(quotes_file, "r") as file:
            quotes = [
                {"quote": line[0], "author": line[1]}
                for line in csv.reader(file, delimiter="|")
            ]

            return random.choice(quotes)

    except Exception as e:
        quote = [
            {
                "quote": "The best way to predict the future is to invent it.",
                "author": "Alan Kay",
            }
        ]
        return random.choice(quote)


def get_weather():
    """
    Get the weather forecast for a given location
    """
    LAT = os.getenv("LOCATION_LAT")
    LON = os.getenv("LOCATION_LON")
    API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

    URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

    try:
        data = json.load(request.urlopen(URL))
        forecast = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "periods": list(),
        }

        for period in data["list"][0:9]:
            forecast["periods"].append(
                {
                    "timestamp": datetime.datetime.fromtimestamp(period["dt"]),
                    "temp": round(period["main"]["temp"], 2),
                    "description": period["weather"][0]["description"].title(),
                }
            )

        return forecast

    except Exception as e:
        print("Somthing went wrong:", e)


def get_random_article():
    """
    Get random wikipedia article
    """
    try:
        article = json.load(
            request.urlopen("https://en.wikipedia.org/api/rest_v1/page/random/summary")
        )
        return article
    except Exception as e:
        print("Something went wrong:", e)


if __name__ == "__main__":

    # Testing quote generation
    print("\nTestig quote generation...\n\n")

    print(f" - Random quote: {get_random_quote()}\n")
    print(f" - Default quote: {get_random_quote(quotes_file=None)}\n")

    print("\nTesting weather retrieval...\n\n")

    # Testing weather forecast
    forcast = get_weather()
    print(f" Weather forecast for {forcast['city']}, {forcast['country']} is...")
    for period in forcast["periods"]:
        print(f" - {period['timestamp']}: {period['temp']}°C, {period['description']}")

    # Testing Random Artilce
    print("\nTestig atricle retrieval...\n\n")
    article = get_random_article()
    print(f"\n\nRandom article: {article['title']}\n")
    print(f"Summary: {article['extract']}")
