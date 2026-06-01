import requests  # type: ignore # pip install requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import os
import re
from dotenv import load_dotenv  # type: ignore # pip install python-dotenv

load_dotenv()

def print_results(results, limit=10):
    print("\n" + "=" * 60)
    print(f"📚 Found {len(results)} results")
    print("=" * 60)

    for i, item in enumerate(results[:limit], start=1):
        print(f"\n[{i}] {item['title']}")
        print("-" * 60)

        if item["authors"]:
            print("👤 Authors :", ", ".join(item["authors"]))

        print("💰 Price   :", f"${item['price']:.2f}" if item["price"] else "N/A")
        print("⭐ Rating  :", item["rating"] if item["rating"] else "N/A")
        print("📝 Reviews :", item["reviews"])

        if item["url"]:
            print("🔗 URL     :", f"https://www.amazon.com{item['url']}")

        if item["image"]:
            print("🖼️ Image  :", item["image"])

    print("\n" + "=" * 60)