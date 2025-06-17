import logging
from pathlib import Path
from time import strftime

ROOT_DIR = Path(__file__).parent
path_to_data = str(ROOT_DIR.joinpath("data", "operations.xlsx")).replace("\\", "\\\\")
time = strftime("%Y-%m-%d %H:%M:%S")
settings = str(ROOT_DIR.joinpath("user_settings.json")).replace("\\", "\\\\")

# logger модуля views.py и utils.py
views_logger = logging.getLogger("views.py")
views_handler = logging.FileHandler(Path.joinpath(ROOT_DIR, "logs", "views_logs.txt"), mode="w", encoding="utf-8")
views_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
views_handler.setFormatter(views_formatter)
views_logger.addHandler(views_handler)
views_logger.setLevel(logging.DEBUG)
views_logger.propagate = False

# logger модуля services.py
services_logger = logging.getLogger("services.py")
services_handler = logging.FileHandler(
    Path.joinpath(ROOT_DIR, "logs", "services_logs.txt"), mode="w", encoding="utf-8"
)
services_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
services_handler.setFormatter(services_formatter)
services_logger.addHandler(services_handler)
services_logger.setLevel(logging.DEBUG)
services_logger.propagate = False

# logger модуля reports.py
reports_logger = logging.getLogger("reports.py")
reports_handler = logging.FileHandler(Path.joinpath(ROOT_DIR, "logs", "reports_logs.txt"), mode="w", encoding="utf-8")
reports_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
reports_handler.setFormatter(reports_formatter)
reports_logger.addHandler(reports_handler)
reports_logger.setLevel(logging.DEBUG)
reports_logger.propagate = False
