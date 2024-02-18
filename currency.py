import requests
from datetime import datetime, timedelta

api_key = '40cafaa0379893a41f9d34404c01db15'
target_currency = 'USD'

def get_last_month_dates():
    current_date = datetime.now()
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    last_month_dates = [first_day_of_last_month + timedelta(days=i) for i in range((last_day_of_last_month - first_day_of_last_month).days + 1)]

    return first_day_of_last_month, last_day_of_last_month

def get_daily_coinlayer_data(api_key, date, target_currency, symbols):
    date_str = date.strftime("%Y-%m-%d")
    url = f'http://api.coinlayer.com/{date_str}?access_key={api_key}&target={target_currency}&symbols={",".join(symbols)}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Ошибка запроса для {date_str}: {response.status_code}")
        return None

def get_currency_data(api_key, start_date, end_date, target_currency, symbols):
    currency_data = []

    current_date = start_date
    while current_date <= end_date:
        coinlayer_data = get_daily_coinlayer_data(api_key, current_date, target_currency, symbols)

        if coinlayer_data and 'rates' in coinlayer_data:
            formatted_date = current_date.strftime("%Y-%m-%d")
            currency_data.append((current_date.day, coinlayer_data['rates'][symbols[0]]))
        else:
            print(f"Не удалось получить данные для {current_date}")

        current_date += timedelta(days=1)

    return currency_data

def getdata(name):
    start_date, end_date = get_last_month_dates()
    data = get_currency_data(api_key, start_date, end_date, target_currency, [name])
    return data

def get_month_and_year():
    current_date = datetime.now()
    russian_month_names = [
        "Январь", "Февраль", "Март", "Апрель",
        "Май", "Июнь", "Июль", "Август",
        "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_name = russian_month_names[current_date.month - 2]
    return f"{month_name} {current_date.year}"


