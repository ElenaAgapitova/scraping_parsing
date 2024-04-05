import requests

url = 'https://jsonplaceholder.typicode.com/posts/1'

response = requests.get(url)
if response.status_code == 200:
    print('ok')
    print(response.text)
else:
    print(response.status_code)
    print('error')

data = {'title': 'GB',
        'body': 'hello world',
        'userId': 1}

post = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
print(post.status_code)
if post.status_code == 201:
    print('ok')
    print(post.text)
else:
    print('error')

data = {'title': 'GB', 'body': 'example put'}

response = requests.put(url, json=data)

print(response.status_code)
print(response.text)

response = requests.delete(url)

print(response.status_code)
print(response.text)
