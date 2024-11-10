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
      s2.run_scraper()
      
    
if __name__ == "__main__":
    main_instance = main()
    main_instance.main()
