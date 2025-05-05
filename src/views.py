from importlib.metadata import pass_none
from time import strftime
import pandas as pd
from pathlib import Path
import openpyxl
from pandas.core.methods.to_dict import to_dict

ROOT_DIR = (Path(__file__).parent.parent)
path_to_data = str(ROOT_DIR.joinpath('data','operations.xlsx')).replace("\\", '\\\\')
time = strftime('%Y-%m-%d %H:%M:%S')

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
    df = pd.read_excel(path_to_xlsx, usecols = ['Номер карты','Сумма операции'])
    sum_dict = {}
    for index, row in df.iterrows():
        # Check if the current card number is already in the dictionary
        if row['Номер карты'] in sum_dict:
            # If it's already in the dictionary, update the values
            sum_dict[row['Номер карты']]['total_spent'] += row['Сумма операции']
            sum_dict[row['Номер карты']]['cashback'] = abs(sum_dict[row['Номер карты']]['total_spent'] / 100)
        else:
            # If it's not in the dictionary, create a new entry
            sum_dict[row['Номер карты']] = {
                'last_digits': row['Номер карты'],
                'total_spent': row['Сумма операции'],
                'cashback': abs(row['Сумма операции'] / 100)
            }
    
    return

def top_transactions(path_to_xlsx):
    df = pd.read_excel(path_to_xlsx, usecols = ['Дата операции','Сумма операции', 'Категория','Описание'])
    max_df = df.groupby('Дата операции')['Сумма операции'].sum().reset_index()
    print(max_df)
    # result = []
    # for el in sum_df.to_dict(orient='records'):
    #     result.append({"last_digits": el['Номер карты'].replace('*', ''),
    #   "total_spent": el['Сумма операции'],
    #   "cashback": el['Кэшбэк']})
    # return result
print(cards(path_to_data))