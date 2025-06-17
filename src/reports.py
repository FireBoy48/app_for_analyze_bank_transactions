import pandas as pd

from config import ROOT_DIR, path_to_data, reports_logger, time
from src.utils import read_xlsx

today, hours = time.split(" ")


def reports_file(name_file: str):
    '''
    Записывает все выданные функцией результаты в файл с названием
    :param name_file: Название файла
    :return: Результат функции
    '''
    reports_logger.info("Запуск декоратора reports_file")

    def reports(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(f"{ROOT_DIR}\\reports\\{name_file}", "a", encoding="utf-8") as f:
                f.write(f"{result}\n")
            reports_logger.info("Данные записаны")
            return result

        return wrapper

    return reports


@reports_file("reports.txt")
def spending_by_weekday(df: list, date: str=today) -> list:
    '''
    Возвращает все операции совершенные в эту дату
    :param df: DataFrame с операциями
    :param date: дата по которой необходимо искать
    :return: Список с операциями
    '''
    reports_logger.info("Запуск функции spending_by_weekday")
    new_list = []
    for item in df.to_dict(orient="records"):
        op_date, op_time = item["Дата операции"].split(" ")
        if op_date == date:
            new_list.append(item)
    reports_logger.info(f"Найдено {len(new_list)} совпадений")
    new_df = pd.DataFrame(new_list)
    return new_df


print(spending_by_weekday(read_xlsx(path_to_data), "31.12.2018"))
