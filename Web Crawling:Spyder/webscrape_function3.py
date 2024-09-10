from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

def scrape_webpage_data3(url, output_path):
    chrome_options = Options()
    chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  #Replace with your Chrome installation path

    # Set up Selenium and the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Open the webpage
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(5)  # Adjust the wait time as needed

    # Use BeautifulSoup with Selenium
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    element_data = []

    # Find the table or any other elements
    elements = soup.find_all(lambda tag: (
        (tag.name in ['h1', 'h2'] and not (
                (tag.name == 'h2' and tag.get('id') == 'dialog-title')
            )
        ) or
        (tag.name == 'div' and all(c in tag.get('class', []) for c in ['courseblock']))
    ))

    for element in elements:
        text = element.get_text().replace('\xa0', ' ').replace('\u200b','').replace('\u00a0',' ').strip()
        if text:
            element_data.append(text)

    combined_data=" ".join(element_data)
        #element_data.append(level_text)
    with open(output_path, 'w') as file:
        file.write(combined_data)

    driver.quit()




