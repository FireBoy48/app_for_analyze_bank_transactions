from unittest.mock import patch

import pandas as pd
import pytest

from config import path_to_data
from src.utils import read_xlsx, rounder


@patch("src.utils.pd.read_excel")
def test_read_xlsx(mock_df):
    fake_file = pd.DataFrame([{"Дата операции": "29.12.2021 15:08:20", "Сумма платежа": -383.0}])
    mock_df.return_value = fake_file
    assert read_xlsx(path_to_data).to_dict(orient="records") == [
        {"Дата операции": "29.12.2021 15:08:20", "Сумма платежа": -383.0}
    ]
    mock_df.assert_called_once_with(path_to_data, usecols=None)


@pytest.mark.parametrize("input_str,expected", [({"a": {"b": 1.234}}, [{"b": 1.23}])])
def test_rounder(input_str, expected):
    assert rounder(input_str) == expected
