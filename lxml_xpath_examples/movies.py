import csv

import pandas as pd
import requests
from fake_useragent import UserAgent
from lxml import html

headers = {
    'User_Agent': UserAgent().random
}

url = 'https://m.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
response = requests.get(url, headers=headers)
print('Scraping...')
print('Status code:', response.status_code)

tree = html.fromstring(response.content)
li_elements = tree.xpath('//li[contains(@class,"cli-parent")]')

ranking_list = []
moved_ranking = []
names_movies = []
years = []
duration = []
age_restrictions = []
marks = []
votes_count = []

for li in li_elements:
    # извлечение рейтинга фильма:
    ranking = li.xpath('.//div[contains(@aria-label, "Ranking ")]')
    ranking_list.append(int(ranking[0].text.strip()))

    # извлечение изменений в рейтинге (количество строк, на которое поднялся или опустился фильм в рейтинге)
    moved_rank = li.xpath('.//span[contains(@aria-label, "Moved ")]/@aria-label')
    if moved_rank:
        if moved_rank[0].split()[1] == 'down':
            moved_ranking.append((-1) * int(moved_rank[0].split()[2]))
        elif moved_rank[0].split()[1] == 'up':
            moved_ranking.append(int(moved_rank[0].split()[2]))
    else:
        moved_ranking.append(0)

    # извлечение названия фильма
    name_movie = li.xpath('.//h3[@class="ipc-title__text"]')
    if name_movie:
        names_movies.append(name_movie[0].text.strip())
    else:
        names_movies.append(None)

    # извлечения года, продолжительности и возрастных ограничений фильма
    parameters = li.xpath('.//span[contains(@class,"sc-b0691f29-8")]')
    if parameters:
        years.append(int(parameters[0].text.strip()))

        if len(parameters) > 1:
            duration.append(parameters[1].text.strip())
        else:
            duration.append(None)

        if len(parameters) > 2:
            age_restrictions.append(parameters[2].text.strip())
        else:
            age_restrictions.append(None)
    # извлечение оценки (среднее количество звезд)
    mark = li.xpath('.//span[contains(@aria-label, "IMDb rating:")]/@aria-label')
    if mark:
        marks.append(float(mark[0].split()[-1]))
    else:
        marks.append(None)

    # извлечение количества голосов
    vote_count = li.xpath('.//span[contains(@class, "ipc-rating-star--voteCount")]')
    if vote_count:
        vote_count_ = vote_count[0].text_content().strip().replace('(', '').replace(')', '')
        if vote_count_[-1] == 'K':
            votes_count.append(float(vote_count_[:-1]) * 10 ** 3)
        elif vote_count_[-1] == 'M':
            votes_count.append(float(vote_count_[:-1]) * 10 ** 6)
        elif vote_count_[-1].isdigit():
            votes_count.append(float(vote_count_))
    else:
        votes_count.append(None)

# формируем словарь из извлеченных данных и записываем в файл top_100_movies.csv
movies_dict = {
    'rank': ranking_list,
    'change_rank': moved_ranking,
    'names_movie': names_movies,
    'year': years,
    'duration': duration,
    'age_restrictions': age_restrictions,
    'mark': marks,
    'vote_count': votes_count
}

with open('top_100_movies.csv', 'w', newline='', encoding='cp1251') as file:
    writer = csv.writer(file)
    writer.writerow(movies_dict.keys())
    for row in zip(*movies_dict.values()):
        writer.writerow(row)

print('The file has been recorded.')
df = pd.DataFrame(movies_dict)
print(df.tail())
