from bs4 import BeautifulSoup
import requests
import prettify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import lxml

GOOGLE_FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSebiEaSXnwot6BBBjybxKvNc23k2BQGdGel6w5LKUOwOFRrqg/viewform?usp=sf_link'
OTODOM_URL = 'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/malopolskie/krakow/krakow/krakow?distanceRadius=0&limit=36&priceMax=3000&roomsNumber=%5BONE%2CTWO%5D&by=DEFAULT&direction=DESC&viewType=listing'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                  " Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,uk;q=0.6,pl;q=0.5",
}

# Getting all information using BeautifulSoup from website OTODOM with filters like: Krakow, price <= 3000, 1&2 beds
# sawing it all in lists

response = requests.get(url=OTODOM_URL, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())

prices = soup.find_all(class_='css-1cyxwvy ei6hyam2')
price_and_sq_m = []
[price_and_sq_m.append(price.getText().replace('\xa0', ' ')) for price in prices]

# prices and square metres are under same class, so I seperated them
all_prices = []
all_sq_m = []
for i in range(len(price_and_sq_m) // 3) :
    all_prices.append(price_and_sq_m[i * 3])

for i in range(len(price_and_sq_m) // 3):
    all_sq_m.append(price_and_sq_m[2 + i * 3])

commissions = soup.find_all(class_='css-5qfobm ei6hyam4')
all_commissions = []
[all_commissions.append(commission.getText().replace('\xa0',' ')) for commission in commissions]

addresses = soup.find_all(class_='css-19dkezj e1n06ry53')
all_addresses = []
[all_addresses.append(address.getText()) for address in addresses]

links =soup.find_all(class_='css-1tiwk2i e1dfeild2')
all_links = []
[all_links.append('https://www.otodom.pl'+link.get('href')) for link in links]

# We get all required information. Opening google forms to fill up all gaps using selenium

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# all information into gaps

for i in range(len(all_addresses)):
    driver.get(url=GOOGLE_FORM_LINK)
    time.sleep(1)

    address_input = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prices_input = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    commission_input = driver.find_element(By.XPATH,
                                           '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    sq_m_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
    send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

    address_input.send_keys(all_addresses[i])
    prices_input.send_keys(all_prices[i])
    commission_input.send_keys(all_commissions[i])
    sq_m_input.send_keys(all_sq_m[i])
    link_input.send_keys(all_links[i])
    send_button.click()

