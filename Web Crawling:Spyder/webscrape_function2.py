from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

def scrape_webpage_data2(url, output_path):
    chrome_options = Options()
    chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  #Replace with your Chrome installation path

    # Set up Selenium and the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Open the webpage
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(3)  # Adjust the wait time as needed

    # Use BeautifulSoup with Selenium
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    element_data = []

    # Find the table or any other elements
    elements = soup.find_all(lambda tag: (
        (
            tag.name in ['p', 'h1', 'h2', 'h3','ol','table','h4'] and  # Include these tags
            not (
                (tag.name == 'h3' and ('footer__title' in tag.get('class', []) and ('footer__title--ghost' in tag.get('class', []) or 'secondary' in tag.get('class', [])))) or
                (tag.name == 'h2' and tag.get('id') == 'dialog-title') or
                (tag.name == 'p' and (
                    'option-desc' in tag.get('class', []) or
                    tag.find('a', class_='option-name') is not None or
                    'Western Sydney University' in tag.get_text()  # Checking for specific text content
                ))
            )
        )
    ))
    for element in elements:
        # Extract text and clean unwanted characters
        text = element.get_text().replace('\xa0', ' ').replace('\u200b',
                                                               '').replace('\u00a0',' ').strip()  # Remove non-breaking spaces and zero-width spaces
        if text:  # Only add non-empty cleaned text
            element_data.append(text)



    tests=soup.find_all('div', id='relatedstructurestextcontainer')

    for test in tests:
        links=test.find_all('li')
        for link in links:
            link_text=link.text.strip()
            element_data.append(link_text)

    combined_data=" ".join(element_data)

    with open(output_path, 'w') as file:
        file.write(combined_data)
    print(element_data)
    driver.quit()





