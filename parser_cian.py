import sqlite3
import time
from datetime import datetime
import requests
from realty import check_database


def get_offer(item):
    offer = {}

    offer["url"] = item["fullUrl"]
    offer["offer_id"] = item["id"]

    timestamp = datetime.fromtimestamp(item["addedTimestamp"])
    timestamp = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
    offer["date"] = timestamp

    offer["price"] = item["bargainTerms"]["priceRur"]
    offer["address"] = item["geo"]["userInput"]
    offer["area"] = item["totalArea"]
    offer["rooms"] = item["roomsCount"]
    offer["floor"] = item["floorNumber"]
    offer["total_floor"] = item["building"]["floorsCount"]

    return offer


def get_offers(data):
    for item in data["data"]["offersSerialized"]:
        offer = get_offer(item)
        check_database(offer)
        # break


def get_json():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    data = '{"jsonQuery":{"region":{"type":"terms","value":[1]},"_type":"flatrent","room":{"type":"terms","value":[1,2,3,4,5,6,9,7]},"engine_version":{"type":"term","value":2},"for_day":{"type":"term","value":"!1"},"is_by_homeowner":{"type":"term","value":true},"sort":{"type":"term","value":"creation_date_desc"}}}'
    response = requests.post('https://api.cian.ru/search-offers/v2/search-offers-desktop/', headers=headers, data=data)
    result = response.json()
    return result


def main():
    data = get_json()
    get_offers(data)


if __name__ == '__main__':
    main()