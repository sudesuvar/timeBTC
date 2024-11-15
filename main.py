import requests
import csv
import time
import os
from datetime import datetime, timedelta
from selenium_yahoo import selenium_yahoo
from coingeckoApi import coingeckoApi

class main:
  def main(self):
      s1 = coingeckoApi()
      s1.run()
      s2 = selenium_yahoo(driver_path= 'C:\\Users\\sudes\\Desktop\\chromedriver-win64\\chromedriver.exe', output_csv='selenium_yahoo.csv')
      s2.run()
      
      output_file = "btcData.csv"
        
      # Dosyanın var olup olmadığını kontrol et
      if not os.path.exists("selenium_yahoo.csv"):
          print("Hata: selenium_yahoo.csv dosyası oluşturulmadı.")
          return
      if not os.path.exists("coingecko_api.csv"):
          print("Hata: coingecko_api.csv dosyası oluşturulmadı.")
          return
        
        # Dosyaları birleştirme işlemi
      with open("coingecko_api.csv", "r") as file1, open("selenium_yahoo.csv", "r") as file2, open(output_file, "w") as outfile:
          outfile.write(file1.read())
          outfile.write("\n")
          outfile.write(file2.read())
        
      print("Dosyalar başarıyla birleştirildi!")

      # Oluşan dosyayı kontrol et ve silme işlemi
      if os.path.exists(output_file):
        try:
          os.remove("coingecko_api.csv")
          os.remove("selenium_yahoo.csv")
        except Exception as e:
          print(f"Dosyalar silinirken bir hata oluştu: {e}")
      else:
        print(f"{output_file} oluşturulamadı. Dosyalar silinmedi.")

      
    
if __name__ == "__main__":
    main_instance = main()
    main_instance.main()
