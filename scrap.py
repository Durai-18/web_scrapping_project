import os.path
from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/web_scrapping/chromedriver/stable/chromedriver")


driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
url = ('https://dev.rentalforincome.com/property/list')

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")  

hotels = []
overall = soup.findAll('div', {'class': "box-footer"}) 
print(len(overall))

for each in overall:
    temp = {}
    name = each.find('h3', {'class': "proptitle"})
    temp['Name'] = name.text
    cash = each.findAll('strong')
    temp['Cash Needed'] = cash[0].text
    temp['Monthly Cash Flow'] = cash [1].text
    hotels.append(temp)

driver.quit()

print(pandas.DataFrame(hotels))