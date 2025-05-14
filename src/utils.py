import pandas as pd


def read_xlsx(path_to_xlsx, *cols):
    if cols == True:
        cols=[*cols]
    else:
        cols = None
    try:
        df = pd.read_excel(path_to_xlsx, usecols=cols)
        if df.empty:
            print("Пустой файл.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []
    return df


def rounder(sum_dict):
    for v in sum_dict.values():
        for k in v:
            if isinstance(v[k], float):
                v[k] = round(v[k], 2)
    return list(sum_dict.values())