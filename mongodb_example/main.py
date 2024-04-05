from pymongo import MongoClient

from scraping import get_data

if __name__ == '__main__':
    client = MongoClient("mongodb://localhost:27017/")
    db = client['movies']
    collection = db['top_250_19_03_24']

    data = get_data()
    collection.insert_many(data)
    print('Data added to the database "Movies"')
    client.close()
