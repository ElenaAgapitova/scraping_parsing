import os
import random

import pandas as pd

from parsing import get_df
from scraping_1 import get_file

FILE_PATH = 'html_content.html'
DATA_PATH = 'books.csv'


def main(file_path, data_path):
    if not os.path.exists(file_path):
        get_file(file_path)

    if not os.path.exists(data_path):
        df = get_df(file_path)
        df.to_csv(data_path, index=False)

    df = pd.read_csv(data_path)
    index = random.randint(1, 1000)
    print("Наименование колонок: ", *df.columns)
    print(f"\nКнига по индексу № {index}:")
    print(df.iloc[index])
    print()
    print(df.head(7))


if __name__ == '__main__':
    main(FILE_PATH, DATA_PATH)
