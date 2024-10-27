from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Chrome tarayıcı için seçenekleri ayarlama
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat

# WebDriver için ChromeDriver'ı belirle
chrome_driver_path = 'C:\\Users\\sudes\\Desktop\\chromedriver-win64\\chromedriver.exe'  # ChromeDriver'ın indirildiği yol

service = Service(executable_path=chrome_driver_path)

# Tarayıcıyı başlat
driver = webdriver.Chrome(service=service, options=chrome_options)

# İstediğin web sayfasına git
driver.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/")

# Sayfanın yüklenmesini bekle
time.sleep(5)

csv_file_path = 'bitcoin_historical_data.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Tablo başlıklarını yaz
    csv_writer.writerow(['Tarih', 'Açılış', 'Yüksek', 'Düşük', 'Kapanış'])
    
    # Verileri çekmek için sürekli döngü
    while True:
        # Web sayfasındaki veriyi çek
        try:
            table = driver.find_element(By.TAG_NAME, "table")  # Tablonun HTML etiketini bul
            rows = table.find_elements(By.TAG_NAME, "tr")  # Tablo satırlarını bul
            
            # Verileri CSV dosyasına yaz
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")  # Satırdaki hücreleri bul
                
                if columns:
                    date = columns[0].text  # Tarih sütunu
                    open_price = columns[1].text  # Açılış fiyatı
                    high_price = columns[2].text  # Yüksek fiyat
                    low_price = columns[3].text  # Düşük fiyat
                    close_price = columns[4].text  # Kapanış fiyatı

                    # Verileri CSV dosyasına yaz
                    csv_writer.writerow([date, open_price, high_price, low_price, close_price])

            # Her hücre için JavaScript ile arka plan rengini değiştir
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                for column in columns:
                    driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", column)  # Arka plan rengini sarı yap
                    time.sleep(0.1)  # Her hücre arasında bekle

            # "Load More" butonunu bul ve tıkla
            load_more_button = driver.find_elements(By.XPATH, "//button[text()='Load More']")
            if load_more_button:
                load_more_button[0].click()  # İlk butona tıkla
                time.sleep(2)  # Yeni verilerin yüklenmesi için bekle
            else:
                break  # Buton yoksa döngüden çık

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            break

    print(f"Veriler {csv_file_path} dosyasına kaydedildi.")

# Tarayıcıyı kapatma komutunu vermeden önce bir süre bekle ki tarayıcı penceresini görebil
time.sleep(10)
driver.quit()  # Tarayıcıyı kapat
