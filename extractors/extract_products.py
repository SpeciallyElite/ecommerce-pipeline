import os
import json
import logging
import datetime
import requests
from datetime import datetime
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s',
    handlers = [
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

url = "https://dummyjson.com/products"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
RAW_DATA_PATH = "data/raw/products"
today_date = datetime.now().strftime("%Y-%m-%d")
today_hour = datetime.now().strftime("%H-%M-%S")
new_directory = os.path.join(RAW_DATA_PATH, today_date)

def tight_session():
    
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429,500,502,503,504],
        allowed_methods=["GET"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def extract_data():
    
    session = tight_session()
    
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    try:
        os.makedirs(new_directory, exist_ok=True)
        
        file_name = f"{today_hour}.json"
        file_path = os.path.join(new_directory, file_name)
    
        with open (file_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f , indent=4)
        
    except Exception as e:
        logger.error(f"An error occured - '{e}'")
        
if __name__ == "__main__":
    extract_data()