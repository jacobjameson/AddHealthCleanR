from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm

# Set up the Selenium WebDriver for Safari
driver = webdriver.Safari()

# Base URL
base_url = "https://addhealth.cpc.unc.edu/documentation/codebook-explorer"

# List of URLs to scrape
urls = [
    base_url + "/#/variables_by_instrument/1",
    base_url + "/#/variables_by_instrument/2",
    base_url + "/#/variables_by_instrument/3",
    base_url + "/#/variables_by_instrument/4",
    base_url + "/#/variables_by_instrument/5"
]

names = ['SCH', 'W1', 'W2', 'W3', 'W4']

for i, main_url in enumerate(urls, start=1):
    # Navigate to the main page
    driver.get(main_url)

    # Wait for the dynamic content to load on the main page
    time.sleep(5)

    # Parse the main page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the relevant rows containing the variables and links
    rows = soup.find_all('tr')

    # Extract variables, links, and question texts
    data = []
    for row in rows:
        cells = row.find_all('td')
        if cells and len(cells) >= 2:  # Check if there are enough cells in the row
            variable = cells[0].get_text().strip()
            question_text = cells[1].get_text().strip()
            link_tag = cells[0].find('a')
            if link_tag:
                link = base_url + link_tag['href']
                data.append({'variable': variable, 'link': link, 'question_text': question_text})

    # Now, visit each link and scrape the codebook data
    for item in tqdm(data, desc=f"Scraping Progress for Instrument {i}"):
        driver.get(item['link'])
        time.sleep(3)  # Wait for the page to load

        # Parse the page with BeautifulSoup
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the table with the codebook data
        table = page_soup.find('table')
        if table:
            rows = table.find_all('tr')
            codebook_data = []
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) >= 2:
                    response_value = cols[0].get_text().strip()
                    response_label = cols[1].get_text().strip()
                    codebook_data.append({'response_value': response_value, 'response_label': response_label})

            item['codebook_data'] = codebook_data

    # Save the data to a JSON file
    with open(f'codebook_data_instrument_{names[i-1]}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Data for Instrument {names[i-1]} saved to codebook_data_instrument_{names[i-1]}.json")

# Close the WebDriver
driver.quit()