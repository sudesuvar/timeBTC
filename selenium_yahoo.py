from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

class selenium_yahoo:
    def __init__(self, driver_path, output_csv):
        self.driver_path = driver_path
        self.output_csv = output_csv

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Web sayfasını aç
            driver.get("https://finance.yahoo.com/quote/BTC-USD/history/")

            # Sayfa yüklenene kadar bekle
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

            # Butonlara tıklama
            try:
                first_button_xpath = '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[1]/div[1]/button/span'
                first_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, first_button_xpath)))
                first_button.click()
                time.sleep(10)  # Animasyonlar için bekleme

                second_button_xpath = '/html/body/div[2]/main/section/section/section/article/div[1]/div[1]/div[1]/div/div/section/div[1]/button[8]'
                second_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, second_button_xpath)))
                second_button.click()
                time.sleep(30)

            except Exception as e:
                print(f"Button click failed: {e}")

            # Verileri CSV dosyasına yazma işlemi
            with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Date", "Open", "High", "Low", "Close"])  # Başlıklar

                previous_row_count = 0
                while True:
                    try:
                        table = driver.find_element(By.TAG_NAME, "table")  # Tabloyu bulma
                        rows = table.find_elements(By.TAG_NAME, "tr")  # Satırları alma

                        # Yeni satırları almak için satır sayısını karşılaştır
                        new_rows = rows[previous_row_count:]  # Yeni satırları al

                        for row in new_rows:
                            columns = row.find_elements(By.TAG_NAME, "td")  # Satırdaki hücreler
                            if columns:
                                date = columns[0].text
                                open_price = columns[1].text
                                high_price = columns[2].text
                                low_price = columns[3].text
                                close_price = columns[4].text

                                # Veriyi CSV'ye yazma
                                csv_writer.writerow([date, open_price, high_price, low_price, close_price])

                                # Her hücreyi sarıya boyama
                                for column in columns:
                                    driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", column)
                                    #time.sleep(0.1)

                        # Yeni satır sayısını kaydet
                        previous_row_count = len(rows)

                        # "Load More" butonu yoksa döngüyü kır
                        break  # Bu örnekte "Load More" butonu yok

                    except Exception as e:
                        print(f"Bir hata oluştu: {e}")
                        break

            print(f"Veriler {self.output_csv} dosyasına kaydedildi.")
        
        finally:
            #time.sleep(5)
            driver.quit()

if __name__ == "__main__":
    #chrome_driver_path = 'C:\\Users\\sudes\\Desktop\\chromedriver-win64\\chromedriver.exe'
    chrome_driver_path = 'C:\\Users\\zeyne\\Desktop\\chromedriver\\chromedriver.exe'
    output_csv_path = "selenium_Yahoo.csv"
    
    scraper = selenium_yahoo(chrome_driver_path,output_csv_path)
    scraper.run()
