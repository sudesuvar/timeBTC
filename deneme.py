from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

class BitcoinPriceScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self.initialize_driver()
        self.csv_file_path = "bitcoin_prices_colored.csv"  # CSV dosyasının adı
        self.previous_row_count = 0

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def open_website(self):
        self.driver.get("https://finance.yahoo.com/quote/BTC-USD/history/")
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Click the specified button before scraping data
        self.click_button()

        self.scrape_data()

    def click_button(self):
        try:
            # İlk buton tıklaması
            first_button_xpath = '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[1]/div[1]/button/span'
            first_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, first_button_xpath)))
            first_button.click()
            time.sleep(2)  # Animasyonlar veya sayfa değişiklikleri için bekleme

            # İkinci buton tıklaması
            second_button_xpath = '/html/body/div[2]/main/section/section/section/article/div[1]/div[1]/div[1]/div/div/section/div[1]/button[8]'
            second_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, second_button_xpath)))
            second_button.click()
            time.sleep(2)  # İkinci tıklama sonrası bekleme

        except Exception as e:
            print(f"Button click failed: {e}")

    def scrape_data(self):
        with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Date", "Open", "High", "Low", "Close"])  # Başlıklar

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

                    # "Load More" butonu yoksa döngüden çık
                    break  # Bu örnekte "Load More" butonu yok

                except Exception as e:
                    print(f"Bir hata oluştu: {e}")
                    break

        print(f"Veriler {self.csv_file_path} dosyasına kaydedildi.")

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
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    chrome_driver_path = 'C:\\Users\\zeyne\\Desktop\\chromedriver\\chromedriver.exe'

    scraper = BitcoinPriceScraper(chrome_driver_path)
    scraper.open_website()
    scraper.close_driver()
