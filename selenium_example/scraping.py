import time
import random
from fake_useragent import UserAgent
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = 'https://www.bookvoed.ru/catalog/psikhologiya-2237'

USER_AGENT = UserAgent().random


def initialize_driver(user_agent: str) -> webdriver:
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)  # запускаем драйвер
    driver.maximize_window()
    return driver


def get_element(driver: webdriver, path: str) -> str | None:
    try:
        return driver.find_element(By.XPATH, path).text.strip().replace('\xc1', '')\
            .replace('\xed', '').replace('\u0306', '')
    except NoSuchElementException:
        return None


def get_links_of_pages(url, driver: webdriver):
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    last_page = int(get_element(driver, '//*[@id="__nuxt"]/div/div[2]/main/div/div/div[2]/div[1]/div[3]/ul/li[8]'))
    link_pages = [url + f'?page={i}' for i in range(1, last_page + 1)]
    return link_pages


def extract_data(driver: webdriver) -> tuple[list[str | None], list[str | None],
                                             list[float | None], list[float | None],
                                             list[float | None]]:
    names, authors, ratings, new_prices, old_prices = [], [], [], [], []
    book_elements = driver.find_elements(By.XPATH, '//div[@class="product-list app-catalog__products"]/div')
    for element in book_elements:
        names.append(get_element(element, ".//div[@class='product-description product-card__description-row']/a"))
        author = (get_element(element, ".//div[@class='product-description product-card__description-row']/ul/li/span"))
        if not author:
            author = (get_element(element, ".//div[@class='product-description "
                                           "product-card__description-row']/ul/li/a"))
        authors.append(author)

        rating = get_element(element, ".//div[@class='product-rating-circle "
                                      "product-rating-circle--five product-card__rating']")
        rating = float(rating) if rating is not None else None
        ratings.append(rating)

        book_new_price = get_element(element, ".//div[contains(@class, 'price-info')]"
                                              "/span[contains(@class, 'price-info__price--sale')]")
        book_new_price = float(book_new_price.replace('₽', '').replace(' ', '')) \
            if book_new_price is not None else None
        new_prices.append(book_new_price)

        book_old_price = get_element(element, ".//div[contains(@class, 'price-info')]"
                                              "/span[contains(@class, 'price-info__old-price--sale')]")
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


def get_full_data_csv(url: str, driver: webdriver):
    links_pages = get_links_of_pages(url, driver)
    full_data = pd.DataFrame()
    for link in links_pages:
        driver.get(link)
        time.sleep(random.randint(1, 2))
        data = extract_data(driver)
        df = get_df(data)
        full_data = pd.concat([full_data, df])
    save_to_csv(full_data, 'psychology.csv', 'cp1251')


def main():
    driver = initialize_driver(USER_AGENT)
    get_full_data_csv(URL, driver)
    driver.quit()


if __name__ == '__main__':
    main()
