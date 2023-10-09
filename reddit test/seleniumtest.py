import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
path = 'C:/Users/user/Desktop/chromedriver'
driver = webdriver.Chrome(path)

driver.get(url = 'https://www.youtube.com/')


#현재 url 얻기
#print(driver.current_url)

#브라우저 닫기
#driver.close()

#브라우저로딩대기
driver.implicitly_wait(time_to_wait=1)