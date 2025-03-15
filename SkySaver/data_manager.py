import requests
import os
class DataManager:
    def __init__ (self):
        self.sheet_api = os.getenv("SHEET_API")
        
    def update_destination_codes(self, sheet_data):
        for city_data in sheet_data:
            row_id = city_data["id"]
            update_endpoint = f"{self.sheet_api}/{row_id}"
            
            new_data = {
                "price": {
                    "iataCode": "TEST"
                }
            }
            
            response = requests.put(url = update_endpoint, json = new_data)
            print(f"Updated row {row_id}: {response.status_code}")