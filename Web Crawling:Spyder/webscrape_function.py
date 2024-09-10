from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

def scrape_webpage_data(url, output_path):
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

    # Find the table or any other elements
    elements = soup.find_all(lambda tag: (
        (
            tag.name in ['p', 'h1', 'h2', 'h3'] and  # Include these tags
            not (
                (tag.name == 'h3' and ('footer__title' in tag.get('class', []) and ('footer__title--ghost' in tag.get('class', []) or 'secondary' in tag.get('class', [])))) or
                (tag.name == 'h2' and tag.get('id') == 'dialog-title') or
                (tag.name == 'p' and (
                    'option-desc' in tag.get('class', []) or
                    tag.find('a', class_='option-name') is not None or
                    'Western Sydney University' in tag.get_text()  # Checking for specific text content
                ))
            )
        ) or
        (tag.name == 'span' and ('label' in tag.get('class', []) or 'sc_courseinline' in tag.get('class', [])))
    ))
    for element in elements:
        # Extract text and clean unwanted characters
        text = element.get_text().replace('\xa0', ' ').replace('\u200b',
                                                               '').replace('\u00a0',' ').strip()  # Remove non-breaking spaces and zero-width spaces
        if text:  # Only add non-empty cleaned text
            element_data.append(text)
    location_table = []
    location = soup.find('table', class_='sc_sctable tbl_location')
    if location:
        rows = location.find('tbody').find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            for column in columns:
                location_table.append(column.text.strip())

    location = soup.find('table', class_='sc_sctable tbl_location_specialisation')
    if location:
        rows = location.find('tbody').find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            for column in columns:
                location_table.append(column.text.strip())

    # Initialize a list to store table data
    tables = soup.find_all('table', class_='sc_plangrid')
    sequence_tables = []

    # Extract data from HTML tables
    for table in tables:
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                row_data = []
                columns = row.find_all(['td', 'th'])
                for column in columns:
                    text = column.get_text(separator=' ', strip=True).replace('\xa0', ' ')  # Remove \xa0
                    row_data.append(text)
                sequence_tables.append(row_data)


    tables = soup.find_all('table', class_='sc_courselist')
    courselist_data = {}

    for idx, table in enumerate(tables):
        variable_name = f'courselist table{idx + 1}'
        courselist_data[variable_name] = []

        rows = table.find('tbody').find_all('tr')
        for row in rows:
            columns = row.find_all(['td', 'th'])
            row_data = [column.text.strip() for column in columns]
            courselist_data[variable_name].append(row_data)

    combined_data = {
        "Elements": [element.get_text(strip=True) for element in elements],
        "Location Table": location_table,
        "Sequence Tables": sequence_tables,
        "Courselist Tables": courselist_data
    }
    combined_data = ""

    combined_data += "Elements:\n"
    for element in element_data:
        combined_data += f"- {element}\n"

    combined_data += "\nLocation Table:\n"
    for location in location_table:
        combined_data += f"- {location}\n"

    combined_data += "\nSequence Tables:\n"
    for table in sequence_tables:
        # Ensure each row is joined correctly
        for row in table:
            combined_data += "".join(row)  # Join the contents of each row with a tab
            combined_data += "\n"

    combined_data += "\nCourselist Tables:\n"
    for table_name, table_data in courselist_data.items():
        combined_data += f"\n{table_name}:\n"
        for row in table_data:
            combined_data += "".join(row)
            combined_data += "\n"
    #combined_json = json.dumps(combined_data, indent=4)

    with open(output_path, 'w') as file:
        file.write(combined_data)

    driver.quit()

