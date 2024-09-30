from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# URL of the webpage
url = 'https://floridalottery.com/games/scratch-offs/games-ending'



# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Set up the Chrome WebDriver
chromedriver_path = r'C:\WebDrivers\chromedriver-win64\chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the URL
driver.get(url)

# Wait for the table to load
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rows-striped')))

# Get the page source after JavaScript has loaded the content
html = driver.page_source

print(driver.page_source)

# Parse the HTML content
soup = BeautifulSoup(html, 'html.parser')

table = soup.find('div', class_="endinggames")

# Extract table headers
headers = [th.text.strip() for th in table.find('thead').find_all('th')]

# Find the tbody with the class 'rows-striped'
tbody = table.find('tbody', class_='rows-striped')

# Extract table rows
rows = []
for row in tbody.find_all('tr', class_='row-rounded'):
    cells = row.find_all(['th', 'td'])
    game_info = cells[0].find('a')
    game_name = game_info.find('span').text.strip()
    game_number = game_info.find('small').text.strip().strip('(#)')
    last_day_to_purchase = cells[1].text.strip()
    last_day_to_redeem = cells[2].text.strip()
    ticket_price = cells[3].text.strip('$')

    rows.append([game_name, game_number, last_day_to_purchase, last_day_to_redeem, ticket_price])

# Close the browser
driver.quit()

# Create a pandas DataFrame
df = pd.DataFrame(rows, columns=['Game Name', 'Game Number', ' last_day_to_purchase', 'last_day_to_redeem', 'Ticket Price'])

# Specify the output file path
output_file = r'C:\Users\jsoto\OneDrive\Documents\My Tableau Repository\Datasources\Lottery\fllottery_02.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)


# Write the DataFrame to the CSV file
df.to_csv(output_file, index=False)

print(f"Data has been successfully written to {output_file}")