import requests
import os
from datetime import datetime, timedelta
from flight_data import FlightData

TOKEN_URL = os.getenv("TOKEN_URL")
IATA_ENDPOINT = os.getenv("IATA_ENDPOINT")
FLIGHT_SEARCH_API = os.getenv("FLIGHT_SEARCH_API")

class FlightSearch:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.token = self.get_new_token()

    def get_new_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }

        response = requests.post(url=TOKEN_URL, headers=headers, data=body)
        response_data = response.json()

        print(f" New token: {response_data['access_token']}")
        print(f"Token expires in {response_data['expires_in']} seconds")

        return response_data['access_token']

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "keyword": city_name,
            "max": "1",
            "include": "AIRPORTS",
        }

        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)

        try:
            code = response.json()["data"][0]["iataCode"]
            print(f" IATA code for {city_name}: {code}")
            return code
        except (IndexError, KeyError):
            print(f"No IATA code found for {city_name}.")
            return "N/A"

    def find_cheapest_flight(self, destination_code):
        today = datetime.today()
        tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        six_months_later = (today + timedelta(days=6*30)).strftime("%Y-%m-%d")

        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": "LON",
            "destinationLocationCode": destination_code,
            "departureDate": f"{tomorrow},{six_months_later}",
            "adults": 1,
            "nonStop": "true",
            "max": 5,
            "currencyCode": "GBP"
        }

        response = requests.get(url=FLIGHT_SEARCH_API, headers=headers, params=query)   
        try:
            flight_data = response.json()["data"][0]  
            price = flight_data["price"]["total"]
            departure_airport = flight_data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            arrival_airport = flight_data["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            departure_date = flight_data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight_data["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0]

            return FlightData(price, departure_airport, arrival_airport, departure_date, return_date)

        except (IndexError, KeyError):
            print("No flights found. Returning default FlightData.")
            return FlightData()
