import json
import sqlite3
import time
from datetime import datetime
import requests
from realty import check_database


def get_offer(item):
    offer = {}

    offer["url"] = "https://www.avito.ru" + item["uri_mweb"]
    offer["offer_id"] = item["id"]

    price = ''.join(item['price'].replace(' ₽ в месяц', '').split())
    title = item['title'].split(', ')
    area = float(title[1].replace(' м²', '').replace(',', '.'))
    rooms = title[0]

    floor_info = title[2].replace(' эт.', '').split('/')
    floor = floor_info[0]
    total_floor = floor_info[-1]

    timestamp = datetime.fromtimestamp(item['time'])
    timestamp = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
    offer["date"] = timestamp

    offer["price"] = price
    offer["address"] = f"{item['location']}, {item['address']}"
    offer["area"] = area
    offer["rooms"] = rooms
    offer["floor"] = floor
    offer["total_floor"] = total_floor

    return offer


def get_offers(data):
    items = data["result"]["items"]
    for item in items:
        if "item" in item["type"]:
            offer = get_offer(item["value"])
            check_database(offer)


def get_json():
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    }

    params = (
        ('key', 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'),
        ('categoryId', '24'),
        ('params[201]', '1060'),
        ('locationId', '107620'),
        ('params[504]', '5256'),
        ('owner[]', 'private'),
        ('sort', 'date'),
        ('page', '1'),
        ('display', 'list'),
        ('limit', '30'),
    )

    url = 'https://m.avito.ru/api/11/items'

    response = requests.get(url=url, headers=headers, params=params)
    data = response.json()

    return data


def main():
    data = get_json()
    get_offers(data)


if __name__ == '__main__':
    main()