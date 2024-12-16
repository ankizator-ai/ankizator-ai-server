from bs4 import BeautifulSoup

import requests
import re

from ninja import Schema

from api.models import Word


class SourceSchema(Schema):
    source: str

def extract_tablepress_content(collection):
    response = requests.get(collection.url)
    if response.status_code != 200:
        print(f"Failed to retrieve URL: {collection.url}")
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
            extracted_data.append(Word(collection=collection, og=polish, tr=english))

    return extracted_data