import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
PROXY = {
    "proxy_url": os.getenv("proxy_url"),
    "urllib3_proxy_kwargs": {"username": os.getenv("proxy_username"), "password": os.getenv("proxy_password")},
}
