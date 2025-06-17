import pandas as pd

from config import views_logger


def read_xlsx(path_to_xlsx: str, *cols: str) -> list:
    '''
    Читает Excel и выводит требуемые колонки
    :param path_to_xlsx: Путь к Excel
    :param cols: Колонки через запятую
    :return: Список словарей из файла
    '''
    views_logger.info("Запуск модуля read_xlsx")
    if cols == True:
        cols = [*cols]
    else:
        cols = None
    try:
        df = pd.read_excel(path_to_xlsx, usecols=cols)
        views_logger.info("Данные получены.")
        if df.empty:
            views_logger.warning("Пустой файл.")
            return []
    except Exception as e:
        views_logger.warning(f"Ошибка: {e}")
        return []
    return df


def rounder(sum_dict: dict) -> list:
    '''
    Округляет все значения в словаре до 2 знаков после ,
    :param sum_dict: Словарь
    :return: Список словарей с округленными значениями
    '''
    for v in sum_dict.values():
        for k in v:
            if isinstance(v[k], float):
                v[k] = round(v[k], 2)
    return list(sum_dict.values())
