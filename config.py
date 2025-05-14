from time import strftime
from pathlib import Path

ROOT_DIR = (Path(__file__).parent)
path_to_data = str(ROOT_DIR.joinpath('data','operations.xlsx')).replace("\\", '\\\\')
time = strftime('%Y-%m-%d %H:%M:%S')
settings = str(ROOT_DIR.joinpath('user_settings.json')).replace("\\", '\\\\')

