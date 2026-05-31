import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup  # pip install beautifulsoup4

# Scraping with Playright (Equivalent to Chromium launch)
async def scrape_jobs():
    async with async_playwright() as p:
        # Launching the browser
        browser = await p.chromium.launch()
        page = await browser.new_page()

        url = "https://www.indeed.com/jobs?q=software+developer&l=New%20York%2C%20NY"
        
        # Go to the URL
        response = await page.goto(url, wait_until="networkidle")
        print(f"HTTP Status: {response.status}")

        if response.status != 200:
            await browser.close()
            return
        
        soup = BeautifulSoup(await page.content(), "html.parser")
        jobs = []
        cards = soup.select(".job-card")

        for card in cards:
            title_el = card.select_one(".job-title")
            company_el = card.select_one(".company")
            location_el = card.select_one(".location")
            link_el = card.select_one("a")
            
            job = {
                "title": title_el.get_text(strip=True) if title_el else None,
                "company": company_el.get_text(strip=True) if company_el else None,
                "location": location_el.get_text(strip=True) if location_el else None,
                "link": link_el["href"] if link_el and link_el.has_attr("href") else None
            }
            jobs.append(job)
            
            for job in jobs:
                print(job)

        await browser.close()

# Execution
if __name__ == "__main__":
    asyncio.run(scrape_jobs())