import random
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

URL = 'https://books.toscrape.com/catalogue/page-1.html'
BASE_URL = 'https://books.toscrape.com/catalogue/'


def get_file(file_name):
    try:
        response = requests.get(URL)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        number_pages = int(soup.find('li', {'class': 'current'}).text.split()[-1])
        html_content = soup.find('ol', {'class': 'row'})

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(html_content))

        for i in range(2, number_pages + 1, 1):
            url_next = f'page-{i}.html'
            url_page = urllib.parse.urljoin(BASE_URL, url_next)
            response = requests.get(url_page)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            with open(file_name, 'a', encoding='utf-8') as file:
                file.write(str(soup.find('ol', {'class': 'row'})))

            time.sleep(random.randint(1, 5))
    except Exception as e:
        print(e)
