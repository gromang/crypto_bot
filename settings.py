import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
PROXY = {
    "proxy_url": os.getenv("proxy_url"),
    "urllib3_proxy_kwargs": {"username": os.getenv("proxy_username"), "password": os.getenv("proxy_password")},
}

intervals = {
    "1 min": 1,
    "5 min": 5,
    "15 min": 15,
    "30 min": 30,
    "1 hour": 60,
    "4 hours": 240,
    "6 hours": 360,
    "12 hours": 720
}