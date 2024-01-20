from selenium import webdriver
from bs4 import BeautifulSoup
import os
import requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time


TARGET_SIZE = (299, 299)

ITEMS = ['Penguin', 'Peacock', 'Cat', 'Crocodile',
         'Giraffe', 'Elephant', 'Gorilla',  'Koala', 'Lion',
         'Tiger', 'Wolf']

ROOT_FOLDER = 'images'

if not os.path.exists(ROOT_FOLDER):
    os.makedirs(ROOT_FOLDER)



def scroll_down(driver):
    # Execute JavaScript to scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def search_and_download(query):
    driver = webdriver.Chrome()
    folder_path = os.path.join(ROOT_FOLDER, query)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    url = f'https://www.pexels.com/search/{query}/'
    driver.get(url)

    try:
        start_time = time.time()

        while True:
            # Scroll down to load more images
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for a short time after each scroll to allow new images to load
            driver.implicitly_wait(2)

            # Check for a timeout 
            if time.time() - start_time > 15:
                print("Timeout reached. Exiting.")
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:

        # Retrieve the page content after it has been modified by JavaScript
        html_content = driver.page_source

        # Close the Webdriver
    driver.quit()

    # Now, you can use BeautifulSoup to parse the HTML as before
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', {'title': "Download"})
    print(f'images scrapped: {len(links)}')

    for i, link in enumerate(links):
        response = requests.get(link.get('href'))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the content of the response (image data)
            # Open the image using PIL
            image = Image.open(BytesIO(response.content))

            # Resize the image to 299x299 pixels
            image = image.resize((299, 299))

            # Specify the local file path where you want to save the image
            img_path = os.path.join(folder_path, f'{i}.jpg')

            image.save(img_path)


if __name__ == '__main__':
    for item in ITEMS:
        print(f"downloading.... [{item}]")
        search_and_download(item)
