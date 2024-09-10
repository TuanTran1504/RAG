from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

def IC_scrape(url,output_path=None):
    chrome_options = Options()
    chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Replace with your Chrome installation path

    # Set up Selenium and the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Open the webpage
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(2)  # Adjust the wait time as needed

    # Use BeautifulSoup with Selenium
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    element_data = []
    elements = soup.find_all(lambda tag: (
            tag.name == 'div' and (
            ('col' in tag.get('class', []) and 'content' in tag.get('class', [])) or
            ('section-optional-header-image-card' in tag.get('class',[]) and 'section-optional-header-image-text' in tag.get(
            'class', []))
    )
    ))
    for element in elements:
        # Extract text and clean unwanted characters
        text = element.get_text().strip()  # Remove non-breaking spaces and zero-width spaces
        if text:  # Only add non-empty cleaned text
            element_data.append(text)
        links = element.find_all('a')
        for link in links:
            href = link.get('href')
            if href:  # Only add non-empty href
                element_data.append(f'{href}')
    page_content = " ".join(element_data)
    title = soup.title.string if soup.title else 'No title found'

    # Get meta description
    description = soup.find('meta', attrs={'name': 'description'})
    description_content = description['content'] if description else 'No description found'
    modified_time = soup.find('meta', attrs={'property': 'article:modified_time'})
    modified_time_content = modified_time['content'] if modified_time else 'No modified time found'
    if len(page_content) > 0:
        full_content = f"Title: {title}\nDescription: {description_content}\nModified Time: {modified_time_content}\n\nPage Content:\n{page_content}"
        print(full_content)
        with open(output_path, 'w') as file:
            file.write(full_content)
    driver.quit()
