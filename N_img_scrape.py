import requests
from bs4 import BeautifulSoup
import os 
from django.utils.text import get_valid_filename
import shutil



Desktop_path = 'E:/Users/harry oh/Desktop'

os.chdir(Desktop_path)

url = "https://nhentai.net"

response = requests.get(url)

soup = BeautifulSoup(response.content,"html.parser")

i = 0 
n_params = []
n_pages = []

if not os.path.exists("Nhentai"):
    
    os.makedirs("Nhentai")
    os.chdir(Desktop_path + "/Nhentai")

else:

    os.chdir(Desktop_path + "/Nhentai")

for params in soup.find_all("a",class_="cover"):
    
    params_text = params.get("href")

    n_params.append(params_text)

doujin_quantity = len(n_params)

while i < doujin_quantity:

    os.chdir(Desktop_path + "/Nhentai")

    redirect = url + n_params[i]

    redirect_response = requests.get(redirect)

    redirect_soup = BeautifulSoup(redirect_response.content,"html.parser")

    temp_page_count = []

    doujin_title = redirect_soup.find("h1").text

    valid_doujin_title = get_valid_filename(doujin_title)

    if not os.path.exists(valid_doujin_title):

        os.makedirs(valid_doujin_title)
        os.chdir(Desktop_path + "/Nhentai" + "/" + valid_doujin_title)

    else:

        i += 1 
        continue

        #shutil.rmtree(Desktop_path + "/Nhentai" + "/" + valid_doujin_title)
        #os.makedirs(valid_doujin_title)
        #os.chdir(Desktop_path + "/Nhentai" + "/" + valid_doujin_title)

    page_count = redirect_soup.find("div", id="thumbnail-container")

    for pages in page_count.find_all("div",class_="thumb-container"):

        temp_page_count.append(pages.text)

    start_page = 1

    for count in temp_page_count:

        redirect_page_url = redirect + str(start_page)

        redirect_page_url_response = requests.get(redirect_page_url)

        redirect_page_soup = BeautifulSoup(redirect_page_url_response.content,"html.parser")

        image_section = redirect_page_soup.find("section",id="image-container")

        image = image_section.find("img")

        image_src = image.get("src")

        filename = image_src.split("/")[-1]

        image_content = requests.get(image_src)

        with open(filename + ".jpg" , "wb") as wf:
            wf.write(image_content.content)        

        start_page += 1

    #total_pages = len(temp_page_count)

    #n_pages.append(total_pages)

    i += 1 










    
    



    



