import requests
from dotenv import load_dotenv
import os
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData

load_dotenv()

API_KEY = os.getenv("API_KEY")
SHEET_API = os.getenv("SHEET_API")


flight_search = FlightSearch()
data_manager = DataManager()

response = requests.get(url=SHEET_API)
data = response.json()
sheet_data = data["prices"]

for city_data in sheet_data:
    if not city_data["iataCode"]:
        city_data["iataCode"] = flight_search.get_destination_code(city_data["city"])

data_manager.update_destination_codes(sheet_data)

for city in sheet_data:
    iata_code = city["iataCode"]
    
    cheapest_flight = flight_search.find_cheapest_flight(iata_code)
    
    if cheapest_flight:
        flight_data = FlightData(
            price=cheapest_flight.price,
            origin_airport=cheapest_flight.origin_airport,
            destination_airport=cheapest_flight.destination_airport,
            out_date=cheapest_flight.out_date,
            return_date=cheapest_flight.return_date
        )

        print(f"\n Destination: {flight_data.destination_airport}")
        print(f"Price: {flight_data.price} GBP")
        print(f" Departure: {flight_data.origin_airport} on {flight_data.out_date}")
        print(f"Return: {flight_data.return_date}")
    else:
        print(f" No flights found for {city['city']} ({iata_code})")
