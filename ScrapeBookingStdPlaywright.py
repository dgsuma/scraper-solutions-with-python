import asyncio
import os
import urllib.parse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup  # pip install beautifulsoup4

async def scrape_booking():
    browser = None

    try:
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch()
                context = await browser.new_context(viewport={'width': 1280, 'height': 800})
                page = await context.new_page()
            except Exception as e:
                print(f"[ERROR] Failed to launch browser: {e}")
                return []

            query = 'New York'
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.booking.com/searchresults.html?ss={encoded_query}"

            # Navigate
            try:
                response = await page.goto(url, wait_until="networkidle", timeout=60000)
                status = response.status if response else "No response"
                print(f"HTTP Status: {status}")
            except Exception as e:
                print(f"[ERROR] Navigation failed: {e}")
                return []

            # Cookie popup
            try:
                await page.wait_for_selector('#onetrust-accept-btn-handler', timeout=5000)
                await page.click('#onetrust-accept-btn-handler')
            except Exception:
                print("[INFO] No cookie popup found")

            # Wait for content
            try:
                await page.wait_for_selector('[data-testid="property-card"]', timeout=15000)
            except Exception as e:
                print(f"[ERROR] Property cards not found: {e}")
                return []

            # Scroll
            try:
                await page.mouse.wheel(0, 4000)
                await asyncio.sleep(2)

                await page.evaluate("""
                    (async () => {
                        await new Promise((resolve) => {
                            let totalHeight = 0;
                            let distance = 100;
                            let timer = setInterval(() => {
                                let scrollHeight = document.body.scrollHeight;
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                                if (totalHeight >= scrollHeight) {
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, 100);
                        });
                    })()
                """)
            except Exception as e:
                print(f"[WARNING] Scrolling failed: {e}")

            # Parse HTML
            try:
                html_content = await page.content()
                print(html_content[:500])

                soup = BeautifulSoup(html_content, "html.parser")
                cards = soup.select('[data-testid="property-card"]')[:10]

                if not cards:
                    print("[ERROR] No cards found in HTML")
                    return []

                results = []

                for card in cards:
                    try:
                        name_el = card.select_one('[data-testid="title"]')
                        rating_el = card.select_one('[data-testid="review-score"]')

                        results.append({
                            "name": name_el.get_text(strip=True) if name_el else None,
                            "rating": rating_el.get_text(strip=True) if rating_el else None
                        })

                    except Exception as e:
                        print(f"[WARNING] Failed to parse card: {e}")
                        continue

            except Exception as e:
                print(f"[ERROR] Parsing failed: {e}")
                return []

            # Output
            if not results:
                print("No results found.")
                return []

            print("\n" + "=" * 80)

            for i, result in enumerate(results, 1):
                name = result.get("name") or "N/A"
                rating = result.get("rating") or "No rating"

                print(f"\n[{i}] {name}")
                print(f"    ⭐ Rating: {rating}")

            print("\n" + "=" * 80)

            return results

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        return []

    finally:
        if browser:
            try:
                await browser.close()
            except Exception as e:
                print(f"[WARNING] Failed to close browser: {e}")

# Run the async function
asyncio.run(scrape_booking())