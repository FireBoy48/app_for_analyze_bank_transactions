import re

from config import path_to_data, services_logger
from src.utils import read_xlsx


def easy_search(path_to_xlsx: str, search: str) -> list:
    '''
    Простой поиск по файлу
    :param path_to_xlsx: Путь к файлу
    :param search: Искомое слово или его отрывок
    :return: Список словарей с найденным обрывком
    '''
    services_logger.info("Запуск модуля easy_search")
    df = read_xlsx(path_to_xlsx)
    flag = 0
    result = []
    for operation in df.to_dict(orient="records"):
        if re.search(search, str(operation["Категория"]), flags=re.I) or re.search(
            search, str(operation["Описание"]), flags=re.I
        ):
            flag = 1
            result.append(operation)
    if len(result) > 0:
        services_logger.info(f"Найдено {len(result)} совпадений")
    else:
        services_logger.info(f"Совпадений не найдено")
    return result


def transfers_by_individuals(path_to_xlsx: str) -> list:
    '''
    Поиск всех переводов
    :param path_to_xlsx: Путь к файлу
    :return: Список словарей с переводами
    '''
    services_logger.info("Запуск модуля transfers_by_individuals")
    data = easy_search(path_to_xlsx, "Переводы")
    result = []
    for operation in data:
        if re.search(r"\D+\s\D\.", str(operation["Описание"]), flags=re.I):
            result.append(operation)
    if len(result) > 0:
        services_logger.info(f"Найдено {len(result)} совпадений")
    else:
        services_logger.info(f"Совпадений не найдено")
    return result


print(transfers_by_individuals(path_to_data))
