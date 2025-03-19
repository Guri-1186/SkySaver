import requests
import os
from flight_search import FlightSearch

class DataManager:
    def __init__(self):
        self.sheet_api = os.getenv("SHEET_API")
        self.flight_search = FlightSearch() 

    def update_destination_codes(self, sheet_data):
        headers = {
            "Content-Type": "application/json",
            
        }
        for city_data in sheet_data:
            row_id = city_data["id"]

            if not city_data["iataCode"]:
                city_data["iataCode"] = self.flight_search.get_destination_code(city_data["city"])

            if not city_data["iataCode"] or city_data["iataCode"] in ["N/A", "Not Found"]:
                print(f"Skipping row {row_id}: No valid IATA code found.")
                continue
            update_endpoint = f"{self.sheet_api}/{row_id}"
            new_data = {
                "price": {
                    "iataCode": city_data["iataCode"]
                }
            }

            response = requests.put(url=update_endpoint, json=new_data, headers=headers)
            if response.status_code == 200:
                print(f" Updated row {row_id} with IATA code: {city_data['iataCode']}")
            else:
                print(f" Failed to update row {row_id}: {response.status_code} - {response.text}")
