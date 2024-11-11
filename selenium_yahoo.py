from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

class seleniumYahoo:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.csv_file_path = "selenium_Yahoo.csv"
    
    def run(self):
        # Initialize the WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Open the Yahoo Finance website
        driver.get("https://finance.yahoo.com/quote/BTC-USD/history/")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Open CSV file to write
        with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Date", "Open", "High", "Low", "Close"])  # Headers

            # Scrape data
            previous_row_count = 0
            while True:
                try:
                    table = driver.find_element(By.TAG_NAME, "table")  # Locate the table
                    rows = table.find_elements(By.TAG_NAME, "tr")  # Find all table rows

                    # Get only new rows
                    new_rows = rows[previous_row_count:]
                    for row in new_rows:
                        columns = row.find_elements(By.TAG_NAME, "td")
                        if columns:
                            # Extract text from each column
                            date = columns[0].text
                            open_price = columns[1].text
                            high_price = columns[2].text
                            low_price = columns[3].text
                            close_price = columns[4].text
                            
                            # Write row to CSV
                            csv_writer.writerow([date, open_price, high_price, low_price, close_price])

                            # Highlight each cell in yellow
                            for column in columns:
                                driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", column)
                                time.sleep(0.1)  # Delay between each cell highlight

                    # Update row count
                    previous_row_count = len(rows)

                    # No "Load More" button in this example, break loop
                    break

                except Exception as e:
                    print(f"Error: {e}")
                    break

        # Close the driver after a delay
        time.sleep(5)
        driver.quit()
        
        print(f"Data saved to {self.csv_file_path}")

#
