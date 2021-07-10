import os
import pathlib
import sys

SERVER_URL = "http://localhost:5000/cel"
HEADER = {
    'Content-Type': 'application/json'
}

PROJECT_BASE_PATH = os.path.dirname(__file__)
PROJECT_BASE_PATH = os.path.dirname(PROJECT_BASE_PATH)
LOG_DIR = os.path.join(PROJECT_BASE_PATH, 'logs')
sys.path.append(PROJECT_BASE_PATH)
pathlib.Path(LOG_DIR).mkdir(exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "cel_sms.log")
LOG_FORMAT = '%(pathname)s:%(lineno)d %(levelname)s - %(message)s'
