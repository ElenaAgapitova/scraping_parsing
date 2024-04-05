import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_data():
    print('Scraping...')
    url = 'https://ru.wikipedia.org/wiki/250_%D0%BB%D1%83%D1%87%D1%88%D0%B8%D1%85_%D1%84%' \
          'D0%B8%D0%BB%D1%8C%D0%BC%D0%BE%D0%B2_%D0%BF%D0%BE_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8_IMDb'

    headers = {
        'User-Agent': UserAgent().random
    }

    response = requests.get(url, headers=headers)
    print(f'Status code: {response.status_code}')

    if response.status_code == 200:
        print('Parsing...')
        soup = BeautifulSoup(response.content, 'html.parser')

        movies_list = soup.find_all('tr')

        data_full = []
        for movie in movies_list[1:]:
            data = {
                'name_movie': movie.find_all('a')[0].text.strip(),
                'year': movie.find_all('a')[1].text.strip(),
                'genre': ', '.join([item.text for item in movie.find_all('td')[4].find_all('a')])

            }

            directors_span = [item.text for item in movie.find_all('td')[3].find_all('span')
                              if item.text != '[en]']
            directors_a = [item.text for item in movie.find_all('td')[3].find_all('a')
                           if item.text != '[en]']

            directors = directors_span if directors_span else directors_a

            if directors:
                data['director'] = ','.join(directors)

            data_full.append(data)
        print('Data ready...')
        return data_full
