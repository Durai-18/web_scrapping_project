import json
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
url = ('https://www.amazon.in/gp/product/B09ZLPH6C8/ref=s9_acss_bw_cg_BAU21_8b1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-16&pf_rd_r=CA0CGGHQV7PXE160AV7B&pf_rd_t=101&pf_rd_p=e1070a0a-470e-4176-9d12-d9368b1f6428&pf_rd_i=1389396031&th=1')

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")


soup = soup.find('div', class_ = "a-section review-views celwidget")

reviews = []

for review in soup:
    temp = {}
    temp["Name"] = review.find('span', class_="a-profile-name").text
    temp["Rating"] = review.find('span', class_="a-icon-alt").text
    review_title = review.find('a', class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
    temp['Review Title'] = review_title.span.text
    temp["Review Date"] = review.find('span', class_="a-size-base a-color-secondary review-date").text
    content = review.find('span', class_ ="a-size-base review-text")
    temp["Review"]=content.span.text
    
    reviews.append(temp)

print(json.dumps(reviews, indent =4))

driver.quit()