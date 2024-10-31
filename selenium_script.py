from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv


class BitcoinDataScraper:
    def __init__(self, driver_path, csv_file_path):
        self.driver_path = driver_path
        self.csv_file_path = csv_file_path
        self.previous_row_count = 0
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def open_website(self):
        self.driver.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/")
        time.sleep(10)  # Sayfanın yüklenmesi için bekle

    def write_to_csv(self):
        with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Tablo başlıklarını yaz
            csv_writer.writerow(['Tarih', 'Açılış', 'Yüksek', 'Düşük', 'Kapanış'])
            self.scrape_data(csv_writer)

    def scrape_data(self, csv_writer):
        while True:
            try:
                table = self.driver.find_element(By.TAG_NAME, "table")  # Tablonun HTML etiketini bul
                rows = table.find_elements(By.TAG_NAME, "tr")  # Tüm tablo satırlarını bul
                
                # Yeni satırları almak için satır sayısını karşılaştır
                new_rows = rows[self.previous_row_count:]  # Sadece yeni eklenen satırları al

                for row in new_rows:
                    self.process_row(row, csv_writer)

                # Şu anki satır sayısını kaydet
                self.previous_row_count = len(rows)

                # "Load More" butonunu bul ve tıkla
                load_more_button = self.driver.find_elements(By.XPATH, "//button[text()='Load More']")
                if load_more_button:
                    load_more_button[0].click()  # İlk butona tıkla
                    time.sleep(5)  # Yeni verilerin yüklenmesi için bekle
                else:
                    break  # Buton yoksa döngüden çık

            except Exception as e:
                print(f"Bir hata oluştu: {e}")
                break

        print(f"Veriler {self.csv_file_path} dosyasına kaydedildi.")
        print(self.previous_row_count)

    def process_row(self, row, csv_writer):
        columns = row.find_elements(By.TAG_NAME, "td")  # Satırdaki hücreleri bul
        if columns:
            date = columns[0].text  # Tarih sütunu
            open_price = columns[1].text  # Açılış fiyatı
            high_price = columns[2].text  # Yüksek fiyat
            low_price = columns[3].text  # Düşük fiyat
            close_price = columns[4].text  # Kapanış fiyatı

            # Verileri CSV dosyasına yaz
            csv_writer.writerow([date, open_price, high_price, low_price, close_price])

            # Her hücreyi sarıya boyama
            for column in columns:
                self.driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", column)  # Arka plan rengini sarı yap
                time.sleep(0.1)  # Her hücre arasında bekle

    def close_driver(self):
        time.sleep(10)  # Sonlandırmadan önce bekle
        self.driver.quit()


if __name__ == "__main__":
    chrome_driver_path = 'C:\\Users\\sudes\\Desktop\\chromedriver-win64\\chromedriver.exe'
    csv_file_path = 'bitcoin_historical_data.csv'
    
    scraper = BitcoinDataScraper(chrome_driver_path, csv_file_path)
    scraper.open_website()
    scraper.write_to_csv()
    scraper.close_driver()
