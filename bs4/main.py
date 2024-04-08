import os
import random

import pandas as pd

from parsing import get_df
from scraping_1 import get_file

FILE_PATH = 'html_content.html'
DATA_PATH = 'books.csv'
DATA_PATH_JSON = 'books.json'


def main(file_path, data_path, data_path_json):
    if not os.path.exists(file_path):
        get_file(file_path)

    if not os.path.exists(data_path) or not os.path.exists(data_path_json):
        df = get_df(file_path)
        if not os.path.exists(data_path):
            df.to_csv(data_path, index=False)
        if not os.path.exists(data_path_json):
            json_data = df.to_json(orient='records', indent=4)
            with open('books.json', 'w', encoding='utf-8', ) as f:
                f.write(json_data)

    df = pd.read_csv(data_path)
    index = random.randint(1, 1000)
    print("Наименование колонок: ", *df.columns)
    print(f"\nКнига по индексу № {index}:")
    print(df.iloc[index])
    print()
    print(df.head(7))


if __name__ == '__main__':
    main(FILE_PATH, DATA_PATH, DATA_PATH_JSON)
