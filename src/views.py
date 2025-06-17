import datetime
import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from config import path_to_data, settings, time, views_logger
from src.utils import read_xlsx, rounder


def greetings(time: str = time) -> str:
    """
    Преобразует время в приветствие
    :param time: время
    :return: Приветствие относительно заданного времени
    """
    date, now = time.split(" ")
    hour, minute, second = map(int, now.split(":"))

    if 5 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 17:
        return "Добрый день"
    if 17 <= hour < 22:
        return "Добрый вечер"
    if 22 <= hour < 24 or 0 <= hour < 5:
        return "Доброй ночи"


def cards(path_to_xlsx: str) -> list:
    """
    Ищет в файле уникальные данные карт и подсчитывает остаток на них и кешбек
    :param path_to_xlsx: путь до файла с транзакциями
    :return: Список уникальных карт
    """
    views_logger.info("Запуск модуля cards")
    df = read_xlsx(path_to_xlsx, "Номер карты", "Сумма операции")
    sum_dict = {}
    for index, row in df.iterrows():
        if not pd.isnull(row["Номер карты"]) and not pd.isnull(row["Сумма операции"]):
            card_number = str(row["Номер карты"])
            transaction_amount = float(row["Сумма операции"])
            last_digits = card_number[1:5]

            if last_digits in sum_dict:
                sum_dict[last_digits]["total_spent"] += transaction_amount
                sum_dict[last_digits]["cashback"] = (
                    abs(sum_dict[last_digits]["total_spent"]) / 100 if transaction_amount < 0 else 0.00
                )
            else:
                sum_dict[last_digits] = {
                    "last_digits": last_digits,
                    "total_spent": transaction_amount,
                    "cashback": (round(abs(transaction_amount) / 100, 2) if transaction_amount < 0 else 0.00),
                }
    return rounder(sum_dict)


def top_transactions(path_to_xlsx: str) -> list:
    """
    Составляет топ 5 трат или пополнений
    :param path_to_xlsx: путь до файла с транзакциями
    :return: Список из 5 трат
    """
    views_logger.info("Запуск модуля top_transactions")
    try:
        df = read_xlsx(path_to_xlsx, "Дата платежа", "Сумма операции", "Категория", "Описание")
        views_logger.info("Данные получены")
        if not df.empty:
            top_list = sorted(list(df.to_dict(orient="records")), key=lambda x: x["Сумма операции"])[0:5]
            return [
                {
                    "date": x["Дата платежа"],
                    "amount": x["Сумма операции"],
                    "category": x["Категория"],
                    "description": x["Описание"],
                }
                for x in top_list
            ]
        else:
            views_logger.warning("Пустой файл")
            return []
    except Exception as e:
        views_logger.warning(f"Ошибка: {e}")
        return []


def currency_rates(settings: str) -> list:
    """
    Составляет список стоимости валют
    :param settings: путь до файла с названиями валют
    :return: список валют с актуальной стоимостью
    """
    views_logger.info("Запуск модуля currency_rates")
    with open(settings, "r", encoding="utf-8") as f:
        json_file = json.load(f)
    views_logger.info("Данные получены")
    result = []
    for currency in json_file["user_currencies"]:
        url = f"https://api.apilayer.com/fixer/convert?to=RUB&from={currency}&amount=1"
        load_dotenv()
        headers = {"apikey": os.getenv("API_KEY_CURRENCY")}
        views_logger.info(f"Подключение к {url}")
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            views_logger.info("Подключение успешно")
            result.append(
                {
                    "currency": currency,
                    "rate": round(float(response.json()["result"]), 2),
                }
            )
        else:
            views_logger.warning(f"Запрос не был успешным. Возможная причина: \n {response.reason}")
            result.append(response.reason)
    return result


def stock_prices(settings: str) -> list:
    """
    Составляет список стоимости акций
    :param settings: путь до файла с названиями компаний
    :return: список акций с актуальной стоимостью
    """
    views_logger.info("Запуск модуля currency_rates")
    with open(settings, "r", encoding="utf-8") as f:
        json_file = json.load(f)
    result = []
    for ticker in json_file["user_stocks"]:
        url = f"https://api.api-ninjas.com/v1/stockprice?ticker={ticker}"
        load_dotenv()
        headers = {"X-Api-Key": os.getenv("API_KEY_TICKERS")}
        views_logger.info(f"Подключение к {url}")
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            views_logger.info("Подключение успешно")
            result.append({"stock": ticker, "rate": float(response.json()["price"])})
        else:
            views_logger.warning(f"Запрос не был успешным. Возможная причина: \n {response.reason}")
            result.append(response.reason)
    return result


def main_page() -> str:
    '''
    Преобразовывает результат всех функций в json
    :return: json со всеми функциями
    '''
    main_result = {
        "greetings": greetings(time),
        "cards": cards(path_to_data),
        "top_transactions": top_transactions(path_to_data),
        "currency_rates": currency_rates(settings),
        "stock_prices": stock_prices(settings),
    }
    return json.dumps(main_result)


n = datetime.datetime.now()
main_dict = json.loads(main_page())
for i, j in main_dict.items():
    print(i, ":")
    if type(j) == list:
        for k in j:
            print(k)
    else:
        print(j)
    print("Времени затрачено:", datetime.datetime.now() - n, "\n")
    n = datetime.datetime.now()
print("Потраченного времени жаль, зато красиво")
