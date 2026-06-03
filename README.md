# Python Scraper Solutions

Standalone Python scraper examples for Amazon, Booking.com, and Indeed. The scripts demonstrate local Playwright scraping, BeautifulSoup parsing, and Evomi-backed scraping through proxies, Scraping Browser, and Scraper API.

This repository is organized as a set of runnable learning/demo scripts rather than a packaged Python application. Each script can be run directly and prints parsed results to the terminal.

## Project Files

| File | Description |
| --- | --- |
| `ScrapeAmazonEvomiCoreResidential.py` | Searches Amazon books through an Evomi residential proxy and parses book title, authors, price, rating, review count, product URL, and image URL. |
| `ScrapeBookingStdPlaywright.py` | Uses local Playwright Chromium to search Booking.com for New York stays, handle the cookie popup when present, scroll results, and parse property names and ratings. |
| `ScrapeBookingEvomiScrapingBrowser.py` | Connects Playwright to Evomi Scraping Browser over CDP, then scrapes Booking.com property names and ratings. |
| `ScrapeIndeedStdPlaywright.py` | Uses local Playwright Chromium to open an Indeed software developer search and parse visible job cards. |
| `ScrapeIndeedEvomiScraperAPI.py` | Sends an Indeed search URL to the Evomi Scraper API, then parses embedded JSON or falls back to HTML selectors for job data. |
| `commands.txt` | Local setup and command notes. This file is ignored by Git. |

## Requirements

- Python 3.14, or another recent Python 3 version supported by your environment
- Playwright browser binaries
- Evomi credentials for the Evomi-based examples

Install the required Python packages:

```powershell
pip install requests beautifulsoup4 python-dotenv playwright
playwright install
```

## Setup

Create and activate a virtual environment:

```powershell
pymanager exec -V:3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install requests beautifulsoup4 python-dotenv playwright
playwright install
```

Create a `.env` file in the project root for the Evomi-backed scripts:

```env
API_KEY=your_evomi_scraper_api_key
EVOMI_ENDPOINT=your_evomi_scraper_api_endpoint
API_KEY_BROWSER=your_evomi_scraping_browser_api_key
BASE_URL_AMAZON=https://www.amazon.com
EVOMI_PROXY_ENDPOINT_HOST=your_evomi_proxy_host
USER_NAME=your_evomi_proxy_username
PASSWORD=your_evomi_proxy_password
```

Do not commit `.env`. It is already excluded by `.gitignore`.

## Running The Scripts

Run the local Playwright Booking.com scraper:

```powershell
python ScrapeBookingStdPlaywright.py
```

Run the Evomi Scraping Browser Booking.com scraper:

```powershell
python ScrapeBookingEvomiScrapingBrowser.py
```

Run the local Playwright Indeed scraper:

```powershell
python ScrapeIndeedStdPlaywright.py
```

Run the Evomi Scraper API Indeed scraper:

```powershell
python ScrapeIndeedEvomiScraperAPI.py
```

Run the Evomi residential proxy Amazon books scraper:

```powershell
python ScrapeAmazonEvomiCoreResidential.py
```

## Output

The scripts currently print results to the terminal.

- Amazon output includes book title, authors, price, rating, review count, product URL, and image URL.
- Booking.com output includes property names and review scores.
- Indeed output includes job title, company, location, salary when available, job URL, and posted date in the Evomi API version.

Search terms and locations are currently hard-coded inside the scripts. To scrape different data, update the relevant query, URL, or payload value in the script you are running.

## Notes

- Website markup changes frequently, so selectors may need occasional updates.
- Some sites use bot detection, CAPTCHAs, rate limits, and region-specific content. The Evomi examples demonstrate proxy, hosted browser, and scraper API approaches for those situations.
- Use these scripts responsibly and follow each website's terms of service, robots.txt guidance, and applicable laws.
- The current scripts do not save data to files. They only print results.

## Git Ignore Policy

The `.gitignore` excludes virtual environments, Python caches, local secrets, logs, local command notes, databases, and common scraper output folders such as `output/`, `outputs/`, `downloads/`, and `data/`.
