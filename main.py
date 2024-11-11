import requests
import csv
import time
from datetime import datetime, timedelta
from selenium_yahoo import seleniumYahoo
from coingeckoApi import coingeckoApi

class main:
  def main(self):
      s1 = coingeckoApi()
      s1.run()
      s2 = seleniumYahoo(driver_path= 'C:\\Users\\sudes\\Desktop\\chromedriver-win64\\chromedriver.exe')
      s2.run()
      
  
      output_file = "btcData.csv"
      with open("coingecko_api.csv", "r") as file1, open("selenium_Yahoo.csv", "r") as file2, open(output_file, "w") as outfile:
        outfile.write(file1.read())
        outfile.write("\n")  
        outfile.write(file2.read())

      print("Dosyalar başarıyla birleştirildi!")
      
      if os.path.exists(output_file):
        try:
          # Dosyaları silme
          os.remove("coingeckoApi.cvs")
          os.remove("selenium_Yahoo.csv")
        except Exception as e:
          print(f"Dosyalar silinirken bir hata oluştu: {e}")
      else:
        print(f" btcData.cvs oluşturulamadı. Dosyalar silinmedi.")


      
    
if __name__ == "__main__":
    main_instance = main()
    main_instance.main()
