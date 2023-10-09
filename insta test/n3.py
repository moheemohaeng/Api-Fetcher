from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import re

import pandas as pd
from datetime import datetime

import csv

collect_in = False

'''
def interceptor(self, request):
    request.headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    request.headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    request.headers["accept-language"] = "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
'''

def prepare():
    options = webdriver.ChromeOptions()
    option_arg = ["--headless", "--no-sandbox", "--disalbe-dev-shm-usage", "disable-infobars", "--disable-gpu"]
    for option in option_arg:
        options.add_argument(option)

    #driver = webdriver.Chrome('/home/iw/work/fo/chromedriver', chrome_options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver.request_interceptor = interceptor

    driver.implicitly_wait(5)
    return driver

'''
def login_na(driver):
    driver.get("https://nid.naver.com/nidlogin.login")
    login = driver.find_element_by_id("id")
    login.clear()
'''

def get_url(driver, nid):
    url = 'https://m.blog.naver.com/BuddyList.naver?blogId=%s' % nid
    driver.get(url)

def extract_ids(source):
    bs = BeautifulSoup(source, 'html.parser')
    links = bs.findAll('a', class_="link")
    ids = []

    for count, link in enumerate(links):
        fid = link['href']
        if fid.startswith("javascript:"): continue
        ids.append(fid.replace('/', ''))
    return ids

def get_friends_na(driver, id_list):
    d = dict()
    for nid in id_list:
        get_url(driver, nid)
        time.sleep(1)
        d[nid] = extract_ids(driver.page_source)
        print("%d/%d" % (len(d), len(id_list))) 
    return d

def login_in(driver):
    username = 'username@daum.net'
    password = 'password'
    # Load page
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    # Login
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button').submit()

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()   # not now
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()              # not now    

def scrape_in(driver, account, text):
    driver.get("https://www.instagram.com/" + account)
    driver.find_element_by_partial_link_text(text).click()

    time.sleep(5)

    pop_up_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    height = 0
    n = 0
    while n < 5:
        height_before = height
        try:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', pop_up_window)
        except:
            pass

        time.sleep(1)
        height = driver.execute_script("return document.querySelectorAll('.jSC57')[0].scrollHeight")
        if height_before < height: n = 0
        else: n += 1

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.findAll('a',['FPmhX','notranslate','_0imsa'])
    return [l.get_text() for l in links]

def get_friends_in(driver, account):
    try:
        follower = scrape_in(driver, account, "팔로워")
        follow = scrape_in(driver, account, "팔로우")
    except:
        follower = []
        follow = []
    return (follower, follow)
    
d = dict()

driver = prepare()

if collect_in:
    login_in(driver)

n = 0
txs = pd.read_csv("C:\\Users\\user\\Desktop\\insta test\\m0720.csv")
for _, row in txs.iterrows():
    #aemail = row[4]
    #bemail = row[5]
    txid = row[0]
    auid = row[1]
    buid = row[2]
    amails = row[3].split('/')
    bmails = row[4].split('/')
    
    n += 1
    if txid >= 1926710:
        continue
    aids = [amail.split("@")[0] for amail in amails]
    bids = [bmail.split("@")[0] for bmail in bmails]

    #print(aids, bids)
    
    for a in aids:
        if a not in d:
            get_url(driver, a)
            time.sleep(1)
            d[a] = extract_ids(driver.page_source)
    for b in bids:
        if b not in d:
            get_url(driver, b)
            time.sleep(1)
            d[b] = extract_ids(driver.page_source)

    afriends = []
    for a in aids: afriends.extend(d[a])

    bfriends = []
    for b in bids: bfriends.extend(d[b])

    print(n, txid, auid, buid, len(aids), len(afriends), len(bids), len(bfriends))
    
    if len(set(aids).intersection(set(bfriends))) or len(set(bids).intersection(set(afriends))): 
        print("found:", txid, auid, buid, aids, afriends, bids, bfriends)
        break


f = open('fr_na.csv', 'w', newline='')
wr = csv.writer(f)
for m in d:
    wr.writerow([m, ",".join(d[m])])
f.close()
