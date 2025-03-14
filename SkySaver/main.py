import requests
from dotenv import load_dotenv
import os
load_dotenv()
from pprint import pprint
from flight_search import FlightSearch
# from data_manager import DataManager
# from flight_data import FlightData
# from notification_manager import NotificationManager

API_KEY = os.getenv ("API_KEY")
API_SECRET = os.getenv ("API_SECRET")
SHEET_API = os.getenv("SHEET_API")

flightSearch = FlightSearch()

response = requests.get(url = SHEET_API)
data = response.json()
sheet_data = data["prices"]


for city_data in sheet_data:
    if not city_data["iataCode"]:
        city_data["iataCode"] = flightSearch.get_destination_code(city_data["city"])
pprint(sheet_data)


# for city_data in sheet_data:
#     if not city_data["iataCode"]:
#         city_data["iataCode"] = "TEST"
# pprint(sheet_data)
