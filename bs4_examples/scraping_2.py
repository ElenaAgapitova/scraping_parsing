import random
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://books.toscrape.com/catalogue/'


def get_number_books(path_file) -> list:
    number_books = []

    try:
        with open(path_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        for item in soup.find_all('div', class_='image_container'):
            url_book = item.find('a')['href']
            url_page = urllib.parse.urljoin(BASE_URL, url_book)
            response = requests.get(url_page)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            number = int(soup.find('p', {'class': 'instock availability'}).text.split()[2][1:])
            number_books.append(number)
            time.sleep(random.randint(2, 5))
        return number_books
    except Exception as e:
        print(e)
