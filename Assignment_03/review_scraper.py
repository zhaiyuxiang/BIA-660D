from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import random

driver = webdriver.Firefox(executable_path=r'C:\Users\yuxia\Documents\geckodriver.exe')
driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM/ref=cm_cr_getr_d_paging_btm_1?sortBy=recent&pageNumber=1&reviewerType=avp_only_reviews')
wait = WebDriverWait(driver, 10)
author_list=[]
date_list=[]
rating_list=[]
review_list=[]
page_number=1

while page_number<=80:
    load_over=wait.until(EC.presence_of_element_located((By.ID,'cm_cr-review_list')))
    time.sleep(random.randint(1,2))
    data_div = driver.find_element_by_id("cm_cr-review_list")
    data_html = data_div.get_attribute('innerHTML')

    soup=bs(data_html,'html5lib')


    author=[i.text for i in soup.find_all('a',{'data-hook':'review-author'})]

    date=[i.text.replace('on ','') for i in soup.find_all('span',{'data-hook':'review-date'})]

    rating=[i.text.replace(' out of 5 stars','') for i in soup.find_all('i',{'data-hook':'review-star-rating'})]

    review=[i.text for i in soup.find_all('span',{'data-hook':'review-body'})]

    for i in range (len(author)):
        author_list.append(author[i])
        date_list.append(date[i])
        rating_list.append(rating[i])
        review_list.append(review[i])

    next_page=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'a-last')))
    next_page.click()
    page_number+=1

driver.quit()


dataset=[]
for i in range(800):
    dataset.append([author_list[i],date_list[i],rating_list[i],review_list[i]])

df=pd.DataFrame(dataset)

df.columns = ['Author','Date','Rating','Review']

for i in range(781,800):
    df.drop([i],inplace=True)

df.to_json('reviews.json')