import requests
from datetime import date, timedelta
import os
import json
from dataclasses import dataclass
from dotenv import load_dotenv

"""
force_get: boolean. if True, always gets info from API
                    otherwise, cached data will be used if available
"""

# Load the .env file


def get_weather(force_get=False):
    load_dotenv()
    API_KEY = os.getenv("WEERLIVE_API_KEY")
    cache_file = "weer.json"
    LOCATION = "Utrecht"
    URL = (
        f"https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie={LOCATION}"
    )

    if not force_get:
        data = get_local_data(cache_file)
        if data:
            print("returning local data")
            return process_data(data)

    try:
        response = requests.get(URL)
        response.raise_for_status()  # Gooit exception bij HTTP errors

        data = response.json()

        # Save data locally for testing
        with open(cache_file, "w") as f:
            json.dump(data, f)

        # Weer data uit response halen
        if "liveweer" in data and len(data["liveweer"]) > 0:
            return process_data(data)

        else:
            print("Geen weerdata gevonden in response")
            return "no data"

    except requests.exceptions.RequestException as e:
        print(f"Error bij API request: {e}")
        return "request exception"
    except ValueError as e:
        print(f"Error bij JSON parsing: {e}")
        return "ValueError"
    except KeyError as e:
        print(f"Verwachte key niet gevonden: {e}")
        return "KeyError"


def get_local_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error parsing json from {filename}")
            return None
        except Exception as e:
            print(f"Error: {e}")
    else:
        return None


@dataclass
class Weather:
    update_date: str
    current_temp: float
    current_text: str
    icon: str
    max_temp: float
    min_temp: float
    rain_percent: int

    tomorrow_rain: int
    tomorrow_max: float
    tomorrow_min: float
    # hour1_temp: float
    # hour2_temp: float
    # hour3_temp: float


def process_data(data):
    live = data["liveweer"][0]
    today = next((d for d in data["wk_verw"] if d["dag"] == today_str()), None)
    tomorrow = next((d for d in data["wk_verw"] if d["dag"] == tomorrow_str()), None)

    weather = Weather(
        live["time"].rsplit(":", 1)[0],
        live["temp"],
        live["verw"],
        live["image"],
        today["max_temp"],
        today["min_temp"],
        today["neersl_perc_dag"],
        tomorrow["neersl_perc_dag"],
        tomorrow["max_temp"],
        tomorrow["min_temp"],
    )
    return weather


def today_str():
    current_day = date.today().strftime("%d-%m-%Y")
    return current_day


def tomorrow_str():
    return (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")


"""
Samenvatting van response:
{
    "api": [
        {
            "bron": "Bron: Weerdata KNMI/NOAA via Weerlive.nl",
            "max_verz": 300,
            "rest_verz": 297
        }
    ],
    "liveweer": [
        {
            "alarm": 0,
            "dauwp": 14.7,
            "gr": 0,
            "gtemp": 16.6,
            "image": "wolkennacht",
            "ldmmhg": 763,
            "lkop": "Er zijn geen waarschuwingen",
            "ltekst": "Er zijn momenteel geen waarschuwingen van kracht.",
            "luchtd": 1016.62,
            "lv": 88,
            "plaats": "Utrecht",
            "samenv": "Licht bewolkt",
            "sunder": "19:46",
            "sup": "07:19",
            "temp": 17.2,
            "time": "19-09-2025 23:38:02",
            "timestamp": 1758317882,
            "verw": "Warm, droog en zonnig. Morgenmiddag enkele (onweers)buien",
            "windbft": 2,
            "windkmh": 8.1,
            "windknp": 4.4,
            "windms": 2.26,
            "windr": "ZZO",
            "windrgr": 153.7,
            "wrsch_g": "-",
            "wrsch_gc": "-",
            "wrsch_gts": 0,
            "wrschklr": "groen",
            "zicht": 39400
        }
    ],
    "uur_verw": [
        {
            "gr": 0,
            "image": "helderenacht",
            "neersl": 0,
            "temp": 17,
            "timestamp": 1758315600,
            "uur": "19-09-2025 23:00",
            "windbft": 2,
            "windkmh": 10,
            "windknp": 6,
            "windms": 3,
            "windr": "ZO",
            "windrgr": 157
        },
        {
            "gr": 0,
            "image": "helderenacht",
            "neersl": 0,
            "temp": 17,
            "timestamp": 1758319200,
            "uur": "20-09-2025 00:00",
            "windbft": 2,
            "windkmh": 10,
            "windknp": 6,
            "windms": 3,
            "windr": "ZO",
            "windrgr": 158
        },
        ...
    ],
    "wk_verw": [
    {
            "dag": "21-09-2025",
            "image": "buien",
            "max_temp": 17,
            "min_temp": 12,
            "neersl_perc_dag": 50,
            "windbft": 3,
            "windkmh": 14,
            "windknp": 8,
            "windms": 4,
            "windr": "Z",
            "windrgr": 208,
            "zond_perc_dag": 16
        },
    ]
}

"""
