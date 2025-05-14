import json
from time import strftime
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import requests
from src.utils import read_xlsx, rounder
from config import time, settings, path_to_data


def greetings(time = time):
    date, now = time.split(' ')
    hour, minute, second = map(int, now.split(':'))

    if 5 <= hour < 12:
        return 'Доброе утро'
    if 12 <= hour < 17:
        return 'Добрый день'
    if 17 <= hour < 22:
        return 'Добрый вечер'
    if 22 <= hour < 24 or 0 <= hour < 5:
        return 'Доброй ночи'



def cards(path_to_xlsx):
    df = read_xlsx(path_to_xlsx,'Номер карты', 'Сумма операции')
    sum_dict = {}
    for index, row in df.iterrows():
        # Проверка на пустые строки
        if not pd.isnull(row['Номер карты']) and not pd.isnull(row['Сумма операции']):
            card_number = str(row['Номер карты'])
            transaction_amount = float(row['Сумма операции'])
            last_digits = card_number[1:5]

            # Проверка на существование ключа в словаре
            if last_digits in sum_dict:
                    sum_dict[last_digits]['total_spent'] += transaction_amount
                    sum_dict[last_digits]['cashback'] = abs(sum_dict[last_digits]['total_spent']) / 100 \
                        if transaction_amount < 0 else 0.00
            else:
                sum_dict[last_digits] = {
                    'last_digits': last_digits,
                    'total_spent': transaction_amount,
                    'cashback': round(abs(transaction_amount) / 100, 2) if transaction_amount < 0 else 0.00
                }
            return rounder(sum_dict)


def top_transactions(path_to_xlsx):
    try:
        df = pd.read_excel(path_to_xlsx, usecols=['Дата платежа', 'Сумма операции', 'Категория', 'Описание'])
        if not df.empty:
            top_list = sorted(list(df.to_dict(orient='records')), key=lambda x: x['Сумма операции'])[0:5]
            return [{"date": x['Дата платежа'], "amount": x['Сумма операции'], "category": x['Категория'],
                     "description": x['Описание']} for x in top_list]
        else:
            print("Пустой файл.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def currency_rates(settings) -> float:
    with open(settings, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
    result = []
    for currency in json_file['user_currencies']:
        url = f"https://api.apilayer.com/fixer/convert?to=RUB&from={currency}&amount=1"
        load_dotenv()
        headers = {"apikey": os.getenv("API_KEY_CURRENCY")}
        # utils_logger.info(f"Подключение к {url}")
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            # utils_logger.info("Подключение успешно")
            result.append({"currency": currency,
                           "rate": round(float(response.json()["result"]), 2)
                          })
        else:
            # utils_logger.info(f"Запрос не был успешным. Возможная причина: \n {response.reason}")
            result.append(response.reason)
    return result

def stock_prices(settings) -> float:
    with open(settings, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
    result = []
    for ticker in json_file['user_stocks']:
        url = f"https://api.api-ninjas.com/v1/stockprice?ticker={ticker}"
        load_dotenv()
        headers = {"X-Api-Key": os.getenv("API_KEY_TICKERS")}
        # utils_logger.info(f"Подключение к {url}")
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            # utils_logger.info("Подключение успешно")
            result.append({"stock": ticker,
                           "rate": float(response.json()["price"])
                          })
        else:
            # utils_logger.info(f"Запрос не был успешным. Возможная причина: \n {response.reason}")
            result.append(response.reason)
    return result

def main_page():
    return {
        'greetings': greetings(time),
        'cards': cards(path_to_data),
        'top_transactions': top_transactions(path_to_data),
        'currency_rates': currency_rates(settings),
        'stock_prices': stock_prices(settings)
    }

print(main_page())