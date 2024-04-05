import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.bookvoed.ru/books?genre=46'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/122.0.0.0 Safari/537.36"


def initialize_driver(user_agent: str) -> webdriver:
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)  # запускаем драйвер
    driver.maximize_window()  # полноэкранный режим
    return driver


def scroll_all_pages(url: str, driver: webdriver):
    driver.get(url)  # открытие страницы в браузере
    wait = WebDriverWait(driver, 10)  # ожидание загрузки страницы
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_elements(By.XPATH, "//div[@class='WI']")[-1].click()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            except ElementNotInteractableException:
                break
        last_height = new_height


def get_element(driver: webdriver, path: str) -> str | None:
    try:
        return driver.find_element(By.XPATH, path).text.strip()
    except NoSuchElementException:
        return None


def extract_data(driver: webdriver) -> tuple[list[str | None], list[str | None],
                                             list[float | None], list[float | None],
                                             list[float | None]]:
    names, authors, ratings, new_prices, old_prices = [], [], [], [], []

    book_elements = driver.find_elements(By.CSS_SELECTOR, '.ci')
    for element in book_elements:
        names.append(get_element(element, ".//a[@class='oYb Ps']"))
        authors.append(get_element(element, ".//div[@class='Qs']"))

        rating = get_element(element, ".//span[@class='lg']")
        rating = float(rating) if rating is not None else None
        ratings.append(rating)

        book_new_price = get_element(element, ".//div[@class='Cg']")
        book_new_price = float(book_new_price.replace('₽', '').replace(' ', '')) \
            if book_new_price is not None else None
        new_prices.append(book_new_price)

        book_old_price = get_element(element, ".//div[@class='Ts']")
        book_old_price = float(book_old_price.replace('₽', '').replace(' ', '')) \
            if book_old_price is not None else None
        old_prices.append(book_old_price)
    return names, authors, ratings, new_prices, old_prices


def get_df(data: tuple):
    return pd.DataFrame({
        'name': data[0],
        'author': data[1],
        'rating': data[2],
        'new_price': data[3],
        'old_price': data[4]
    })


def save_to_csv(df: pd.DataFrame, filename: str, encoding: str):
    df.to_csv(filename, index=False, encoding=encoding)


def main():
    driver = initialize_driver(USER_AGENT)
    scroll_all_pages(URL, driver)
    data = extract_data(driver)
    df = get_df(data)
    print(df.head())
    print(df.info())
    save_to_csv(df, 'children_books_bookvoed.csv', 'cp1251')
    driver.quit()


if __name__ == '__main__':
    main()
