import json
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RV_LINK = os.environ['RV_LINK']
RV_TOKEN = os.environ['RV_TOKEN']

RV_CERT_PATH = Path(__file__).resolve().parent / os.environ['RV_CERT_PATH']
API_RESPONSES_PATH = Path(__file__).resolve().parent / os.environ['API_RESPONSES_PATH']
EXTEND_FILTERS_PATH = Path(__file__).resolve().parent / os.environ['EXTEND_FILTERS_PATH']

BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND=os.environ['BASE_INCIDENTS_COUNT_FOR_CHECK_TO_BIND']
BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT=os.environ['BASE_INCIDENTS_COUNT_FOR_CHECK_TO_APPLICANT']
BASE_INCIDENT_FIELDS = os.environ['BASE_INCIDENT_FIELDS']
BASE_INCIDENT_NOT_CLOSE_FILTER = json.loads(os.environ['BASE_INCIDENT_NOT_CLOSE_FILTER'])
BASE_INCIDENT_CREATED_FILTER = json.loads(os.environ['BASE_INCIDENT_CREATED_FILTER'])
REFRESH_RATE = os.environ['REFRESH_RATE']

BASE_USER_FIELDS = os.environ['BASE_USER_FIELDS']
BASE_FILTER_FOR_USERS = json.loads(os.environ['BASE_FILTER_FOR_USERS'])

ASSET_ID_USERS = os.environ['ASSET_ID_USERS']
