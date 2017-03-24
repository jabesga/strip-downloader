from bs4 import BeautifulSoup
import requests
import shutil
import os

# all_url = []
# 
# def get_all_url(year, month, day):
#     url = f'http://dilbert.com/strip/{year}-{month:02}-{day:02}'
#     with open('urls.txt', 'a') as f:
#         f.write(url + '\n')
#     all_url.append(url)

def download_comic(year, month, day):
    
    url = f'http://dilbert.com/strip/{year}-{month:02}-{day:02}'
    print(f'Looking {url}')

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        comic_title = soup.find_all("a", class_="comic-title-link")

        # If you  try to access an URL that doesn't exist it will redirect to the main page, so url will be different to the comic-title-link
        if comic_title[0]["href"] == url: 
            print(f'Downloading {year}-{month:02}-{day:02}')
            images = soup.find_all("img", class_="img-responsive img-comic")

            # Get the extension
            extension = requests.get(images[0]["src"]).headers['content-type'].split('/')[-1]
            
            response = requests.get(images[0]["src"], stream=True)
            with open("comics/" + str(f'{year}-{month:02}-{day:02}_dilbert.{extension}'), 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            
    # Sometimes it happens
    except requests.exceptions.ConnectionError:
        print("Error. Trying again...")
        download_comic(year, month, day)

    
ENDING_YEAR = 2017
year = 1992
month = 1
day = 8

if not os.path.exists("comics/"):
    os.makedirs("comics/")

while year != ENDING_YEAR:
    if month > 12:
        year += 1
        month = 1
        day = 1
    if day > 31:
        month += 1
        day = 1

    #get_all_url(year, month, day)
    download_comic(year, month, day)
    day += 1

