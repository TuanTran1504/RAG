from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
from webscrape_function2 import scrape_webpage_data2
# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Replace with your Chrome installation path

# Set up Selenium and the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open the webpage
driver.get('https://hbook.westernsydney.edu.au/')

# Wait for the page to load completely
time.sleep(3)  # Adjust the wait time as needed

# Use BeautifulSoup with Selenium
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract all relative paths
exclude_paths = ["/subject-search/","/archives/"]

# Extract all relative paths excluding 'mailto:' links and specific excluded paths
relative_paths = []
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    # Check if the href is a relative path, not a mailto link, and not in the exclude list
    if not href.startswith('http') and not href.startswith('https') and not href.startswith('mailto:') and href not in exclude_paths:
        relative_paths.append(href)

# Remove duplicates
unique_paths = list(set(relative_paths))

for path in unique_paths:
    # Check if the path starts with '/programs' or '/majors-minors'
    if path.startswith(('/subject-details')):
        # Construct the full URL
        url = 'https://hbook.westernsydney.edu.au' + path

        # Define the output file path
        output_path = '/Users/dinhtuantran/Documents/Python/Test/Scrapping/Data/subject-detail/' + path.strip('/').replace('/',' ') + '.txt'

        # Call the scraping function
        scrape_webpage_data2(url, output_path)
