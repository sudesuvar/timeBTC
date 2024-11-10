import requests
import csv
import time
from datetime import datetime, timedelta

class coingeckoApi:
    def __init__(self, file_path='coingecko_api.csv', days=90, requests_count=3, currency="usd"):
        self.url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        self.file_path = file_path
        self.days = days
        self.requests_count = requests_count
        self.currency = currency

    def run(self):
        end_date = datetime.now()
        
        # Create and write header row in CSV file
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Date', 'Price'])

        # Fetch and write data for each time interval
        for _ in range(self.requests_count):
            start_date = end_date - timedelta(days=self.days)
            print(f"Fetching data for {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

            # Prepare parameters and make request to the API
            params = {
                "vs_currency": self.currency,
                "from": int(start_date.timestamp()),
                "to": int(end_date.timestamp())
            }
            response = requests.get(f"{self.url}/range", params=params)

            # Process the API response and write data to CSV
            if response.status_code == 200:
                data = response.json()
                if "prices" in data:
                    with open(self.file_path, mode='a', newline='', encoding='utf-8') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        for entry in data["prices"]:
                            timestamp = entry[0] / 1000  # Convert milliseconds to seconds
                            date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))
                            price = entry[1]
                            csv_writer.writerow([date, price])

                    print(f"{len(data['prices'])} entries added for {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
                else:
                    print("Error: 'prices' key not found in JSON response.")
            else:
                print(f"Error: API request failed with status code {response.status_code}")

            # Update end_date for the next request interval
            end_date = start_date
            time.sleep(1)  # Wait between API requests

        print(f"All data has been saved to {self.file_path}")

# Usage
if __name__ == "__main__":
    handler = coingeckoApi()
    handler.run()
