import requests
import csv
import time
from datetime import datetime, timedelta

class BitcoinDataHandler:
    def __init__(self, file_path='bitcoin_combined_data.csv', days=90, requests_count=3, currency="usd"):
        self.url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        self.file_path = file_path
        self.days = days
        self.requests_count = requests_count
        self.currency = currency

    def fetch_data(self, start_date, end_date):
        params = {
            "vs_currency": self.currency,
            "from": int(start_date.timestamp()),
            "to": int(end_date.timestamp())
        }
        response = requests.get(f"{self.url}/range", params=params)
        if response.status_code == 200:
            data = response.json()
            if "prices" in data:
                return data["prices"]
            else:
                print("Error: 'prices' key not found in JSON response.")
        else:
            print(f"Error: API request failed with status code {response.status_code}")
        return []

    def write_to_csv(self, data):
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            for entry in data:
                timestamp = entry[0] / 1000  # Convert milliseconds to seconds
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))
                price = entry[1]
                csv_writer.writerow([date, price])

    def fetch_and_save(self):
        end_date = datetime.now()
        # Başlık satırını dosyaya ekleyin
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Tarih', 'Fiyat'])

        for _ in range(self.requests_count):
            start_date = end_date - timedelta(days=self.days)
            print(f"Fetching data for {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

            # API'den verileri çek ve CSV'ye yaz
            prices = self.fetch_data(start_date, end_date)
            if prices:
                self.write_to_csv(prices)
                print(f"{len(prices)} entries added for the period {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

            # Bir sonraki aralık için bitiş tarihini güncelle
            end_date = start_date
            time.sleep(1)  # API talepleri arasında bekleme

        print(f"All data has been saved to {self.file_path}")

# Kullanım
if __name__ == "__main__":
    handler = BitcoinDataHandler()
    handler.fetch_and_save()
