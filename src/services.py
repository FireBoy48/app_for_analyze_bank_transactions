import re

from src.utils import read_xlsx
from config import path_to_data

def easy_search(path_to_xlsx, search):
        df = read_xlsx(path_to_xlsx)
        flag=0
        result = []
        for operation in df.to_dict(orient='records'):
                if (re.search(search, str(operation['Категория']),flags=re.I) or
                        re.search(search, str(operation['Описание']),flags=re.I)):
                        flag=1
                        result.append(operation)
        return result


def transfers_by_individuals(path_to_xlsx):
        data = easy_search(path_to_data, 'Переводы')
        result = []
        for operation in data:
                if re.search(r'\D+\s\D\.', str(operation['Описание']), flags=re.I):
                        flag = 1
                        result.append(operation)
        return result

otvet = transfers_by_individuals(path_to_data)
for strok in otvet:
        print(strok)