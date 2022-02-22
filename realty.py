import sqlite3
import time
import requests
from config import token, chat_id


def check_database(offer):
    offer_id = offer["offer_id"]
    with sqlite3.connect('realty.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT offer_id FROM offers WHERE offer_id = (?)
        """, (offer_id,))
        result = cursor.fetchone()
        if result is None:
            send_telegram(offer)
            cursor.execute("""
                INSERT INTO offers
                VALUES (NULL, :url, :offer_id, :date, :price,
                    :address, :area, :rooms, :floor, :total_floor)
            """, offer)
            connection.commit()
            print(f'Объявление {offer_id} добавлено в базу данных')


def format_text(offer):
    title = f"{offer['rooms']}, {offer['area']} м2, {offer['floor']}/{offer['total_floor']} эт."

    d = offer['date']
    date = f"{d[8:10]}.{d[5:7]} в {d[11:16]}"

    text = f"""{offer['price']} ₽
<a href='{offer['url']}'>{title}</a>
{offer['address']}
{date}"""

    return text


def send_telegram(offer):
    text = format_text(offer)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url=url, data=data)
    print(response)


def main():
    pass


if __name__ == '__main__':
    main()