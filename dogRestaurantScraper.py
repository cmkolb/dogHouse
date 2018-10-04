import os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# default bringfide.com search for dog-friendly restaurants in Pittsburgh, PA
urlbase = "https://www.bringfido.com/restaurant/city/pittsburgh_pa_us/?distance=20&sort=popularity"

# open chrome webdriver window
chromepath = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/chromedriver'
driver = webdriver.Chrome(chromepath)
# program in random weight that will range from 1-3 seconds.
driver.implicitly_wait(10)
# open page
driver.get(urlbase)

import time
patience_time = 30
load_more_xpath = '//*[@id="browse-itemsprimary"]/li[2]/button/span/span[2]'

while(True):
    try:
        load_more_button = driver.find_element_by_xpath("//*[@id='more-results']")
        time.sleep(2)
        load_more_button.click()
        time.sleep(5)
    except Exception as e:
        print(e)
        break
time.sleep(20)

# grab all the restaurant results
restID = []
restNAME = []
restCITY = []
restDESCRIPTION = []

wait = WebDriverWait(driver, 10)

while(True):
    loading_xpath="//div[contains(@class,'info-ctn')]"
    loading = wait.until(EC.visibility_of_element_located((By.XPATH,loading_xpath)))
    currentPageRestaurants = driver.find_elements_by_xpath("//div[contains(@class,'info-ctn')]")
    for restaurant in currentPageRestaurants:
        rest_id_xpath = ".//a[contains(@itemprop,'url')]" # href
        rest_name1_xpath = rest_id_xpath+"//span" # text
        rest_name2_xpath = rest_id_xpath # text
        rest_city_xpath = ".//a[contains(@href, '/restaurant/city')]" # text
        rest_description_xpath = ".//div[contains(@class,'description character-limit')]" # text

        try:
            restaurant_id = restaurant.find_element_by_xpath(rest_id_xpath).get_attribute('href')
        except:
            restaurant_id = "NA"

        try:
            restaurant_name = restaurant.find_element_by_xpath(rest_name1_xpath).text
        except:
            pass
        try:
            restaurant_name = restaurant.find_element_by_xpath(rest_name2_xpath).text
        except:
            restaurant_name = "NA"

        try:
            restaurant_city = restaurant.find_element_by_xpath(rest_city_xpath).text
        except:
            restaurant_city = "NA"

        try:
            restaurant_description = restaurant.find_element_by_xpath(rest_description_xpath).text
        except:
            restaurant_description = "NA"

        restID.append(restaurant_id)
        restNAME.append(restaurant_name)
        restCITY.append(restaurant_city)
        restDESCRIPTION.append(restaurant_description)

    print('Complete')
    break

pghDogRestaurants = pd.DataFrame({'id': restID, 'name': restNAME, 'city': restCITY, 'description': restDESCRIPTION})

pghDogRestaurants.to_csv('pghDogRestaurants.csv')
print('All done')
driver.quit()

pghDogRestaurants.head
pghDogRestaurants.shape
