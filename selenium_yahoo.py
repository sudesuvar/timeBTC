from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import datetime

class BitcoinDateSelector:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def open_website(self):
        self.driver.get("https://www.investing.com/crypto/bitcoin/historical-data")
        time.sleep(10)  # Sayfanın yüklenmesi için bekle
        self.set_date_range()  # Tarih aralığını ayarla
        time.sleep(5)  # Uygulama sonrası bekle

    def set_date_range(self):
        start_date = "2014-10-12"  # Yeni başlangıç tarihi (YYYY-MM-DD formatında)
        # Son tarih bugünün tarihi
        end_date = datetime.now().strftime("%Y-%m-%d")  # Bugünün tarihi (YYYY-MM-DD formatında)

        try:
            # Tarih seçiciye tıklayın
            self.driver.find_element(By.XPATH, '//div[contains(@class, "flex flex-1 items-center gap-3.5")]').click()
            time.sleep(2)

            # Başlangıç tarihini ayarlayın
            start_input = self.driver.find_element(By.XPATH, '//input[@type="date"]')  # İlk tarih input'unu bul
            start_input.clear()  # Var olan metni temizle
            start_input.send_keys(start_date)  # Başlangıç tarihini girin
            time.sleep(1)

            # Bitiş tarihini ayarlamayın, mevcut değeri koruyun
            end_input = self.driver.find_element(By.XPATH, '(//input[@type="date"])[2]')  # İkinci tarih input'unu bul
            current_end_date = end_input.get_attribute('value')  # Mevcut bitiş tarihini al
            print(f"Mevcut bitiş tarihi: {current_end_date}")  # Mevcut bitiş tarihini yazdır

            # Tarih aralığını uygula
            apply_button = self.driver.find_element(By.XPATH, '//button[text()="Apply"]')
            apply_button.click()
            time.sleep(5)  # Uygulama işlemi için bekleyin

            # "Apply" butonunun yanındaki elementi bul ve tıklayın
            self.driver.find_element(By.XPATH, '//span[text()="Apply"]').click()  # Tıklanacak elementin XPath'i
            time.sleep(5)  # İşlem sonrası bekleyin
        except Exception as e:
            print(f"Tarih aralığı ayarlanırken bir hata oluştu: {e}")

    def close_driver(self):
        time.sleep(5)  # Sonlandırmadan önce bekle
        self.driver.quit()

if __name__ == "__main__":
    chrome_driver_path = 'C:\\Users\\zeyne\\Desktop\\chromedriver\\chromedriver.exe'  # ChromeDriver yolunu ayarlayın

    date_selector = BitcoinDateSelector(chrome_driver_path)
    date_selector.open_website()
    date_selector.close_driver()
