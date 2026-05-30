import asyncio
import os
import urllib.parse
from playwright.async_api import async_playwright
from dotenv import load_dotenv # type: ignore
from bs4 import BeautifulSoup  # pip install beautifulsoup4
# Load environment variables from .env
load_dotenv()