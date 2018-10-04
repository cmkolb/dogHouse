import os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# default bringfide.com search for dog-friendly parks in Pittsburgh, PA
urlbase = "https://www.bringfido.com/attraction/city/pittsburgh_pa_us/?distance=20&sort=popularity"

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

# grab all the park results
parkID = []
parkNAME = []
parkCITY = []
parkDESCRIPTION = []

wait = WebDriverWait(driver, 10)

while(True):
    loading_xpath="//div[contains(@class,'info-ctn')]"
    loading = wait.until(EC.visibility_of_element_located((By.XPATH,loading_xpath)))
    currentPageParks = driver.find_elements_by_xpath("//div[contains(@class,'info-ctn')]")
    for park in currentPageParks:
        park_id_xpath = ".//a[contains(@itemprop,'url')]" # href
        park_name1_xpath = park_id_xpath+"//span" # text
        park_name2_xpath = park_id_xpath # text
        park_city_xpath = ".//a[contains(@href, '/attraction/city')]" # text
        park_description_xpath = ".//div[contains(@class,'description character-limit')]" # text

        try:
            park_id = park.find_element_by_xpath(park_id_xpath).get_attribute('href')
        except:
            park_id = "NA"

        try:
            park_name = park.find_element_by_xpath(park_name1_xpath).text
        except:
            pass
        try:
            park_name = park.find_element_by_xpath(park_name2_xpath).text
        except:
            park_name = "NA"

        try:
            park_city = park.find_element_by_xpath(park_city_xpath).text
        except:
            park_city = "NA"

        try:
            park_description = park.find_element_by_xpath(park_description_xpath).text
        except:
            park_description = "NA"

        parkID.append(park_id)
        parkNAME.append(park_name)
        parkCITY.append(park_city)
        parkDESCRIPTION.append(park_description)

    print('Complete')
    break

pghDogParks = pd.DataFrame({'id': parkID, 'name': parkNAME, 'city': parkCITY, 'description': parkDESCRIPTION})

now = time.strftime("%Y%m%d-%H%M%S")
output_csv = 'pghDogParks_'+now+'.csv'
pghDogParks.to_csv(output_csv)
print('All done')
driver.quit()
