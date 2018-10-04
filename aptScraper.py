import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.apartments.com/pittsburgh-pa/pet-friendly-dog/"

# To get the html contents
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
r = requests.get(base_url, headers=headers)

c = r.content

# To parse the html
soup = BeautifulSoup(c,"html.parser")

# To extract the first and last page numbers
paging = soup.find("div",{"id":"placardContainer"}).find("div",{"id":"paging"}).find_all("a")
start_page = paging[1].text
last_page = paging[len(paging)-2].text
web_content_list = []

for page_number in range(int(start_page),int(last_page) + 1):

    # To form the url based on page numbers
    url = base_url+str(page_number)+"/.html"
    r = requests.get(base_url+str(page_number)+"/",headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    # To extract the Title and the Location
    placard_header = soup.find_all("header",{"class":"placardHeader"})

    # To extract the Rent, No of Beds and Phone Number
    placard_content = soup.find_all("section",{"class" :"placardContent"})

    # To process property by property by looping for large placards
    for item_header,item_content in zip(placard_header,placard_content):
        # To store the information to a dictionary
        web_content_dict = {}

        web_content_dict["title"]=item_header.find("a",{"class":"placardTitle"}).text.replace("\r","").replace("\n","")
        web_content_dict["address"] = item_header.find("div",{"class":"location"}).text
        web_content_dict["price"] = item_content.find("span",{"class":"altRentDisplay"}).text
        web_content_dict["beds"] = item_content.find("span",{"class":"unitLabel"}).text
        web_content_dict["phone"] = item_content.find("div",{"class":"phone"}).find("span").text

        # To store the dictionary to into a list
        web_content_list.append(web_content_dict)

    # To extract the Title and the Location
    placard_silver = soup.find_all("article",{"class":"silver placard"})

    # process property by propoerty for small placards
    for item in placard_silver:

        # To store the information to a dictionary
        web_content_dict = {}

        web_content_dict["title"] = item.find("a",{"class":"placardTitle"}).text.replace("\r","").replace("\n","")
        web_content_dict["address"] = item.find("div",{"class":"location"}).text
        web_content_dict["price"] = item.find("span",{"class":"altRentDisplay"}).text
        web_content_dict["beds"] = item.find("span",{"class":"unitLabel"}).text
        web_content_dict["phone"] = item.find("div",{"class":"phone"}).find("span").text

        # To store the dictionary to into a list
        web_content_list.append(web_content_dict)

    # To extract the Title and the Location
    placard_prosumer = soup.find_all("article",{"class":"prosumer placard"})

    # process property by propoerty for small placards
    for item in placard_prosumer:

        # To store the information to a dictionary
        web_content_dict = {}

        web_content_dict["title"] = item.find("a",{"class":"placardTitle"}).text.replace("\r","").replace("\n","")
        web_content_dict["address"] = web_content_dict["title"]+", "+item.find("div",{"class":"location"}).text
        web_content_dict["price"] = item.find("span",{"class":"altRentDisplay"}).text
        web_content_dict["beds"] = item.find("span",{"class":"unitLabel"}).text

        try:
            web_content_dict["phone"] = item.find("div",{"class":"phone"}).find("span").text
        except:
            web_content_dict["phone"] = "NA"

        # To store the dictionary to into a list
        web_content_list.append(web_content_dict)

    # To extract the Title and the Location
    placard_basic = soup.find_all("article",{"class":"basic placard"})

    # process property by propoerty for small placards
    for item in placard_basic:

        # To store the information to a dictionary
        web_content_dict = {}

        web_content_dict["title"] = item.find("a",{"class":"placardTitle"}).text.replace("\r","").replace("\n","")

        if item.find("div",{"class":"location"}).text.startswith("Pittsburgh, PA") or item.find("div",{"class":"location"}).text.startswith("Munhall, PA"):
            web_content_dict["address"] = web_content_dict["title"]+", "+item.find("div",{"class":"location"}).text
        else:
            web_content_dict["address"] = item.find("div",{"class":"location"}).text

        web_content_dict["price"] = item.find("span",{"class":"altRentDisplay"}).text
        web_content_dict["beds"] = item.find("span",{"class":"unitLabel"}).text

        try:
            web_content_dict["phone"] = item.find("div",{"class":"phone"}).find("span").text
        except:
            web_content_dict["phone"] = "NA"

        # To store the dictionary to into a list
        web_content_list.append(web_content_dict)

    # To extract the Title and the Location
    placard_tierTwo = soup.find_all("article",{"class":"tierTwo placard"})

    # process property by propoerty for small placards
    for item in placard_tierTwo:

        # To store the information to a dictionary
        web_content_dict = {}

        web_content_dict["title"] = item.find("a",{"class":"placardTitle"}).text.replace("\r","").replace("\n","")

        if item.find("div",{"class":"location"}).text.startswith("Pittsburgh, PA") or item.find("div",{"class":"location"}).text.startswith("Munhall, PA"):
            web_content_dict["address"] = web_content_dict["title"]+", "+item.find("div",{"class":"location"}).text
        else:
            web_content_dict["address"] = item.find("div",{"class":"location"}).text

        try:
            web_content_dict["price"] = item.find("span",{"class":"altRentDisplay"}).text
        except:
            web_content_dict["price"] = "NA"

        try:
            web_content_dict["beds"] = item.find("span",{"class":"unitLabel"}).text
        except:
            web_content_dict["beds"] = "NA"

        try:
            web_content_dict["phone"] = item.find("div",{"class":"phone"}).find("span").text
        except:
            web_content_dict["phone"] = "NA"

        # To store the dictionary to into a list
        web_content_list.append(web_content_dict)

# To make a dataframe with the list
df = pd.DataFrame(web_content_list)
df.shape

# To write the dataframe to a csv file
now = time.strftime("%Y%m%d-%H%M%S")
output_csv = 'pghDogApts_'+now+'.csv'
df.to_csv(output_csv)
