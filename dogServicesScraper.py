import os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# default bringfide.com search for dog-friendly restaurants in Pittsburgh, PA
urlbase = "https://www.bringfido.com/resource/city/pittsburgh_pa_us/?ql=on&"

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
serviceID = []
serviceNAME = []
serviceCITY = []
serviceDESCRIPTION = []

wait = WebDriverWait(driver, 10)

while(True):
    loading_xpath="//div[contains(@class,'info-ctn')]"
    loading = wait.until(EC.visibility_of_element_located((By.XPATH,loading_xpath)))
    currentPageServices = driver.find_elements_by_xpath("//div[contains(@class,'info-ctn')]")
    for service in currentPageServices:
        service_id_xpath = ".//a[contains(@itemprop,'url')]" # href
        service_name1_xpath = service_id_xpath+"//span" # text
        service_name2_xpath = service_id_xpath # text
        service_city_xpath = ".//a[contains(@href, '/resource/city')]" # text
        service_description_xpath = ".//div[contains(@class,'description character-limit')]" # text

        try:
            service_id = service.find_element_by_xpath(service_id_xpath).get_attribute('href')
        except:
            servicet_id = "NA"

        try:
            service_name = service.find_element_by_xpath(service_name1_xpath).text
        except:
            pass
        try:
            service_name = service.find_element_by_xpath(service_name2_xpath).text
        except:
            service_name = "NA"

        try:
            service_city = service.find_element_by_xpath(service_city_xpath).text
        except:
            service_city = "NA"

        try:
            service_description = service.find_element_by_xpath(service_description_xpath).text
        except:
            service_description = "NA"

        serviceID.append(service_id)
        serviceNAME.append(service_name)
        serviceCITY.append(service_city)
        serviceDESCRIPTION.append(service_description)

    print('Complete')
    break

pghDogServices = pd.DataFrame({'id': serviceID, 'name': serviceNAME, 'city': serviceCITY, 'description': serviceDESCRIPTION})

pghDogServices.to_csv('pghDogServices.csv')
print('All done')
driver.quit()

pghDogServices.head
pghDogServices.shape
