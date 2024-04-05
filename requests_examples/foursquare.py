import requests
from decouple import config

api_key = config('FOURSQUARE_KEY')

category = input('Введите интересующую категорию (например, coffee, museum, park, restaurant, cafe): ')
url = f'https://api.foursquare.com/v3/places/search?' \
      f'query={category}&ll=59.97%2C30.39&open_now=true&sort=DISTANCE'

headers = {
    "accept": "application/json",
    "Authorization": api_key,
}

response = requests.get(url, headers=headers)
data = response.json()

for i, item in enumerate(data['results'], 1):
    print(f"{i}. Название: {item['name']} || адрес: {item['location']['formatted_address']} || "
          f"рейтинг: {item.get('rating', 'не указан')}")
    print()
