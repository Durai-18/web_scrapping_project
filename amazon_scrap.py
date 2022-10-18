import logging
import json 
import os.path 
import time 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import TimeoutException


def find_reviews(tv):
	html = driver.page_source 
	soup = BeautifulSoup(html, "lxml") 
	soup = soup.findAll('div', {'class': "a-section review aok-relative"}) 

	reviews = []
	result = []
	reviews.append({"Product Name": [tv, result] })  
	time.sleep(5) 

	for review in soup: 
		time.sleep(5) 
		temp = {} 
		temp["Name"] = review.find('span', {'class':"a-profile-name"}).text  
		temp["Rating"] = review.find('span', class_="a-icon-alt").text 
		review_title = review.find('a', class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold") 
		temp['Review Title'] = review_title.span.text 
		temp["Review Date"] = review.find('span', class_="a-size-base a-color-secondary review-date").text 
		content = review.find('div', class_ ="a-row a-spacing-small review-data") 
		span = content.findAll('span') 
		temp["Review"]=span[1].text 

		result.append(temp) 

	print(json.dumps(reviews, indent =4)) 
	driver.close() 
	driver.switch_to.window(driver.window_handles[0])
	
## Setup chrome options 
chrome_options = Options() 
chrome_options.add_argument("--headless") # Ensure GUI is off 
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument('--disable-dev-shm-usage') 
homedir = os.path.expanduser("~") 
webdriver_service = Service(f"{homedir}/web_scrapping/chromedriver/stable/chromedriver") 
 
 
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options) 
driver.maximize_window()
url = ('https://www.amazon.in') 
 
drive = driver.get(url) 
search_tv = driver.find_element(By.NAME, "field-keywords") 
search_tv.send_keys("Sony Bravia 189 cm (75 inches) 4K Ultra HD Smart LED Google TV KD-75X80K (Black)") 
search_tv.send_keys(Keys.RETURN) 
time.sleep(5) 
html = driver.page_source 
soup = BeautifulSoup(html, "lxml") 
soup1 = soup.findAll('span', {'class': "a-size-medium a-color-base a-text-normal"}) 
tv_list = [] 
for s in soup1:
	tv_list.append(s.text.strip())

print(json.dumps(tv_list, indent =2))

for tv in tv_list:
	try:
		time.sleep(5)
		driver.implicitly_wait(15)
		tv_name = WebDriverWait(driver, 10).until(
		EC.visibility_of_element_located((By.LINK_TEXT, tv))
		).click()
		driver.switch_to.window(driver.window_handles[1])

		driver.implicitly_wait(10)
		next_page = WebDriverWait(driver, 10).until(
		EC.visibility_of_element_located((By.LINK_TEXT, "See all reviews"))
		)
		if next_page != None:
			next_page.click() 
		else:
			pass
		
		find_reviews(tv)
		
	except TimeoutException:
		print("Time taken to find page content exceeded max time")
		find_reviews(tv)

time.sleep(5) 
driver.quit()