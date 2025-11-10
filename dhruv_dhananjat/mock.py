# pip install supermemory
from supermemory import Supermemory
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("SUPERMEMORY_API_KEY")

client = Supermemory(
    api_key=api_key,
    base_url="https://api.supermemory.ai/"
)


