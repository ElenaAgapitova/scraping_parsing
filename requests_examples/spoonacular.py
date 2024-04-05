import requests
from decouple import config

apiKey = config('API_KEY')

# url = 'https://api.spoonacular.com/recipes/complexSearch?query=pasta&number=2'
url = 'https://api.spoonacular.com/recipes/random?number=1'

query_parameters = {
    "apiKey": apiKey
}

response = requests.get(url, params=query_parameters)

print(response.text)
