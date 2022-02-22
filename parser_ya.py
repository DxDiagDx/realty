import sqlite3
import time
from datetime import datetime
import requests
from realty import check_database


def get_json():
    params = (
        ('sort', 'DATE_DESC'),
        ('rgid', '741964'),
        ('type', 'RENT'),
        ('category', 'APARTMENT'),
        ('agents', 'NO'),
        ('_pageType', 'search'),
        ('_providers',
         ['seo', 'queryId', 'forms', 'filters', 'filtersParams', 'direct', 'mapsPromo', 'newbuildingPromo',
          'refinements', 'search', 'react-search-data', 'searchHistoryParams', 'searchParams', 'searchPresets',
          'serpDirectPicType', 'showSurveyBanner', 'seo-data-offers-count', 'related-newbuildings', 'breadcrumbs',
          'ads', 'categoryTotalOffers', 'footer-links', 'site-special-projects']),
        ('crc', 'u4f6278deddd331b5068e5d14a357bfb2'),
    )

    response = requests.get('https://realty.yandex.ru/gate/react-page/get/', params=params)
    data = response.json()

    return data


def get_offer(item):
    offer = {}

    offer["url"] = item["shareUrl"]
    offer["offer_id"] = item["offerId"]

    offer_date = ''
    if item.get("updateDate"):
        offer_date = item["updateDate"].replace('T', ' ').replace('Z', '')
    else:
        offer_date = item["creationDate"].replace('T', ' ').replace('Z', '')
    offer["date"] = offer_date

    offer["price"] = item["price"]["value"]
    offer["address"] = item["location"]["address"]
    offer["area"] = item["area"]["value"]
    offer["rooms"] = item["roomsTotalKey"]
    offer["floor"] = item["floorsOffered"][0]
    offer["total_floor"] = item["floorsTotal"]

    return offer


def get_offers(data):
    entities = data["response"]["search"]["offers"]["entities"]
    for item in entities:
        offer = get_offer(item)
        check_database(offer)
        # break


def main():
    data = get_json()
    get_offers(data)


if __name__ == '__main__':
    main()