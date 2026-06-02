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
    
def parse_amazon_html(html, search_term):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    items = soup.select('[data-component-type="s-search-result"]')

    for el in items:
        title_recipe = el.select_one('[data-cy="title-recipe"]')

        rating_el = el.select_one('i.a-icon-star-mini .a-icon-alt')
        rating_text = rating_el.get_text(strip=True) if rating_el else ""

        price_el = el.select_one('.a-price .a-offscreen')
        price_text = price_el.get_text(strip=True) if price_el else ""

        title = "Unknown Title"
        authors = []
        url = None

        if title_recipe:
            h2 = title_recipe.find("h2")
            if h2:
                title = h2.get_text(strip=True)

            authors = [
                a.get_text(strip=True)
                for a in title_recipe.select('.a-row.a-size-base.a-color-secondary a')
                if a.get_text(strip=True)
            ]

            link = title_recipe.find("a")
            if link:
                url = link.get("href")

        price = float(re.sub(r"[^\d.]", "", price_text)) if price_text else None
        rating = float(rating_text.split(" ")[0]) if rating_text else None

        reviews = 0
        reviews_el = el.select_one('a[aria-label*="ratings"]')
        if reviews_el and reviews_el.has_attr("aria-label"):
            reviews = int(re.sub(r"\D", "", reviews_el["aria-label"]))

        image_el = el.select_one("img.s-image")
        image = image_el.get("src") if image_el else None

        results.append({
            "searchTerm": search_term,
            "title": title,
            "authors": authors,
            "url": url,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "image": image
        })

    return results   