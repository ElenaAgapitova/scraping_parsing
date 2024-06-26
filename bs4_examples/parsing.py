import pandas as pd
from bs4 import BeautifulSoup

from scraping_2 import get_number_description_books


def get_df(path_file) -> pd.DataFrame:
    rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    name_book = []
    price_book = []
    rating = []

    try:
        number_books, description_books = get_number_description_books(path_file)

        with open(path_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        for item in soup.find_all('article', class_='product_pod'):
            name_book.append(item.find('h3').find('a')['title'])
            rating.append(rating_dict.get(item.find('p')['class'][1], 0))
            price_book.append(float(item.find('div', class_='product_price')
                                    .find('p', class_='price_color').text.strip()[1:]))

        data = {
            'name_book': name_book,
            'rating': rating,
            'price': price_book,
            'description': description_books,
            'in_stock': number_books
        }

        df = pd.DataFrame(data)
        df.columns = data.keys()
        return df
    except Exception as e:
        print(e)
