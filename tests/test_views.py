import json
import os
from unittest.mock import Mock, call, patch

import pandas as pd
import pytest

from config import path_to_data, settings
from src.views import (cards, currency_rates, greetings, main_page,
                       stock_prices, top_transactions)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("31.12.2021 01:23:42", "Доброй ночи"),
        ("31.12.2021 07:23:42", "Доброе утро"),
        ("31.12.2021 12:23:42", "Добрый день"),
        ("31.12.2021 17:23:42", "Добрый вечер"),
    ],
)
def test_greetings(input_str, expected):
    assert greetings(input_str) == expected


@patch("src.views.read_xlsx")
def test_cards(mock_df):
    fake_file = pd.DataFrame(
        [
            {"Номер карты": "*5091", "Сумма операции": -200.0},
            {"Номер карты": "*5091", "Сумма операции": -120.0},
            {"Номер карты": "*7891", "Сумма операции": -120.0},
        ]
    )
    mock_df.return_value = fake_file
    assert cards(path_to_data) == [
        {"last_digits": "5091", "total_spent": -320.0, "cashback": 3.2},
        {"last_digits": "7891", "total_spent": -120.0, "cashback": 1.2},
    ]
    mock_df.assert_called_once_with(path_to_data, "Номер карты", "Сумма операции")


@patch("src.views.read_xlsx")
def test_top_transactions(mock_df):
    fake_file = pd.DataFrame(
        [
            {
                "Дата платежа": "21.03.2019",
                "Сумма операции": -190044.51,
                "Категория": "Переводы",
                "Описание": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "Дата платежа": "23.03.2019",
                "Сумма операции": 190020.51,
                "Категория": "Переводы",
                "Описание": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "Дата платежа": "25.03.2019",
                "Сумма операции": -190044.51,
                "Категория": "Переводы",
                "Описание": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "Дата платежа": "27.03.2019",
                "Сумма операции": 190020.51,
                "Категория": "Переводы",
                "Описание": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "Дата платежа": "29.03.2019",
                "Сумма операции": -44.51,
                "Категория": "Переводы",
                "Описание": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "Дата платежа": "31.03.2019",
                "Сумма операции": 20.51,
                "Категория": "Переводы",
                "Описание": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
        ]
    )
    mock_df.return_value = fake_file
    assert top_transactions(path_to_data) == [
        {
            "amount": -190044.51,
            "category": "Переводы",
            "date": "21.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": -190044.51,
            "category": "Переводы",
            "date": "25.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": -44.51,
            "category": "Переводы",
            "date": "29.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": 20.51,
            "category": "Переводы",
            "date": "31.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": 190020.51,
            "category": "Переводы",
            "date": "23.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
    ]
    mock_df.assert_called_once_with(path_to_data, "Дата платежа", "Сумма операции", "Категория", "Описание")


def test_currency_rates():
    moke_req_usd = Mock()
    moke_req_usd.status_code = 200
    moke_req_usd.json.return_value = {
        "date": "2018-02-22",
        "historical": "",
        "info": {"rate": 79.778, "timestamp": 1519328414},
        "query": {"amount": 1, "from": "RUB", "to": "USD"},
        "result": 79.778,
        "success": True,
    }

    moke_req_eur = Mock()
    moke_req_eur.status_code = 200
    moke_req_eur.json.return_value = {
        "date": "2018-02-22",
        "historical": "",
        "info": {"rate": 92.191, "timestamp": 1519328414},
        "query": {"amount": 1, "from": "RUB", "to": "EUR"},
        "result": 92.191,
        "success": True,
    }

    with patch("src.views.requests.request") as mock_request:
        mock_request.side_effect = [moke_req_usd, moke_req_eur]
        assert currency_rates(settings) == [
            {"currency": "USD", "rate": 79.78},
            {"currency": "EUR", "rate": 92.19},
        ]

        headers = {"apikey": os.getenv("API_KEY_CURRENCY")}
        url_1 = "https://api.apilayer.com/fixer/convert?to=RUB&from=USD&amount=1"
        url_2 = "https://api.apilayer.com/fixer/convert?to=RUB&from=EUR&amount=1"
        expected_calls = [
            call("GET", url_1, headers=headers),
            call("GET", url_2, headers=headers),
        ]
        mock_request.assert_has_calls(expected_calls, any_order=False)
        assert mock_request.call_count == 2


def test_stock_prices():
    moke_req_aapl = Mock()
    moke_req_aapl.status_code = 200
    moke_req_aapl.json.return_value = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "price": 196.45,
        "exchange": "NASDAQ",
        "updated": 1706302801,
        "currency": "USD",
    }

    moke_req_amzn = Mock()
    moke_req_amzn.status_code = 200
    moke_req_amzn.json.return_value = {
        "ticker": "AMZN",
        "name": "Amazon Inc.",
        "price": 212.1,
        "exchange": "NASDAQ",
        "updated": 1706302801,
        "currency": "USD",
    }

    moke_req_googl = Mock()
    moke_req_googl.status_code = 200
    moke_req_googl.json.return_value = {
        "ticker": "GOOGL",
        "name": "Google Inc.",
        "price": 174.67,
        "exchange": "NASDAQ",
        "updated": 1706302801,
        "currency": "USD",
    }

    moke_req_msft = Mock()
    moke_req_msft.status_code = 200
    moke_req_msft.json.return_value = {
        "ticker": "MSFT",
        "name": "Microsoft Inc.",
        "price": 474.96,
        "exchange": "NASDAQ",
        "updated": 1706302801,
        "currency": "USD",
    }

    moke_req_tsla = Mock()
    moke_req_tsla.status_code = 200
    moke_req_tsla.json.return_value = {
        "ticker": "TSLA",
        "name": "Tesla Inc.",
        "price": 325.31,
        "exchange": "NASDAQ",
        "updated": 1706302801,
        "currency": "USD",
    }

    with patch("src.views.requests.request") as mock_request:
        mock_request.side_effect = [
            moke_req_aapl,
            moke_req_amzn,
            moke_req_googl,
            moke_req_msft,
            moke_req_tsla,
        ]
        assert stock_prices(settings) == [
            {"stock": "AAPL", "rate": 196.45},
            {"stock": "AMZN", "rate": 212.1},
            {"stock": "GOOGL", "rate": 174.67},
            {"stock": "MSFT", "rate": 474.96},
            {"stock": "TSLA", "rate": 325.31},
        ]

        headers = {"X-Api-Key": os.getenv("API_KEY_TICKERS")}
        url_1 = "https://api.api-ninjas.com/v1/stockprice?ticker=AAPL"
        url_2 = "https://api.api-ninjas.com/v1/stockprice?ticker=AMZN"
        url_3 = "https://api.api-ninjas.com/v1/stockprice?ticker=GOOGL"
        url_4 = "https://api.api-ninjas.com/v1/stockprice?ticker=MSFT"
        url_5 = "https://api.api-ninjas.com/v1/stockprice?ticker=TSLA"
        expected_calls = [
            call("GET", url_1, headers=headers),
            call("GET", url_2, headers=headers),
            call("GET", url_3, headers=headers),
            call("GET", url_4, headers=headers),
            call("GET", url_5, headers=headers),
        ]
        mock_request.assert_has_calls(expected_calls, any_order=False)
        assert mock_request.call_count == 5


@patch("src.views.stock_prices")
@patch("src.views.currency_rates")
@patch("src.views.top_transactions")
@patch("src.views.cards")
@patch("src.views.greetings")
def test_main_page(
    mock_greetings,
    mock_cards,
    mock_top_transactions,
    mock_currency_rates,
    mock_stock_prices,
):
    mock_greetings.return_value = 1
    mock_cards.return_value = 2
    mock_top_transactions.return_value = 3
    mock_currency_rates.return_value = 4
    mock_stock_prices.return_value = 5
    assert json.loads(main_page()) == {
        "greetings": 1,
        "cards": 2,
        "top_transactions": 3,
        "currency_rates": 4,
        "stock_prices": 5,
    }
