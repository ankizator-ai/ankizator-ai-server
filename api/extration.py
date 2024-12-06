from bs4 import BeautifulSoup

import requests
import re


def extract_tablepress_content(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve URL: {url}")
        return None

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find table with an ID that matches 'tablepress-<random_number>'
    table = soup.find('table', id=re.compile(r'tablepress-\d+'))

    if not table:
        print("Table not found.")
        return None

    extracted_data = []

    # Loop through rows (ignoring the header row)
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) == 2:
            polish = columns[0].get_text(strip=True)
            english = columns[1].get_text(strip=True)
            extracted_data.append({"pl": polish, "en": english})

    return extracted_data