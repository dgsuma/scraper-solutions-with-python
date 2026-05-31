import os
import re
import json
import requests # type: ignore
from bs4 import BeautifulSoup #
from datetime import datetime
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()

def display_jobs_clean(jobs):
    if not jobs:
        print("\n[!] No jobs found to display. \n")
        return
    
    # Define column widths
    t_width = 30 # Title
    c_width = 20 # Company
    l_width = 20 # Location
    s_width = 15 # Salary
    p_width = 12 # Posted Date
    
    # Table header
    header = f"{'TITLE':<{t_width}} | {'COMPANY':<{c_width}} | {'LOCATION':<{l_width}} | {'SALARY':<{s_width}} | {'POSTED-DATE':<{p_width}}"
    divider = '-' * len(header)
    
    print("\n" + divider)
    print(header)
    print(divider)
    
    # Table rows
    for job in jobs[:10]:
        # We use .get() and slicing [0:width-3] to ensure long text doesn't break the table
        title = (job.get('jobTitle') or 'N/A')
        title = (title[:t_width-3] + '...') if len(title) > t_width else title

        company = (job.get('company') or 'N/A')
        company = (company[:c_width-3] + '...') if len(company) > c_width else company

        location = (job.get('location') or 'N/A')
        location = (location[:l_width-3] + '...') if len(location) > l_width else location

        salary = str(job.get('salary', 'Not listed'))
        salary = (salary[:s_width-3] + '...') if len(salary) > s_width else salary

        posted = (job.get('postedDate', 'Unknown'))

        print(f"{title:<{t_width}} | {company:<{c_width}} | {location:<{l_width}} | {salary:<{s_width}} | {posted:<{p_width}}")
        
        print(divider)
        print(f"Total results: {len(jobs)}\n")
        
    def scrape_indeed(html):
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        # 1. Locate the script tag containing the initial data
        # look for script with id 'mosaic-data' or containing 'window._initialData' 
        script_tag = soup.find('script', id='mosaic-data') or \
                    soup.find('script', string=re.compile(r'window\._initialData'))
        if script_tag and script_tag.string:
            script_content = script_tag.string
            try:
                # try multiple patterns (mimicking your js regex)
                match = re.search(r'window\._initialData\s*=\s*({.*?});', script_content, re.DOTALL)
                
                if not match:
                    # Fallback pattern
                    match = re.search(r'({.*"jobData".*})', script_content, re.DOTALL)
                    
                if not match:
                    raise ValueError("JSON pattern not found in script")
                
                json_raw = match.group(1)
                data = json.loads(json_raw) 
                
                # Navigate the JSON structure with safe gets
                # Python's dict.get() or nested access
                job_list = (data.get('hostQuerExecutionResult', {})
                            .get('data', {})
                            .get('jobData', {})
                            .get('results', [])) or \
                            data.get('jobData', {}).get('results', [])
                
                for item in job_list:
                    job = item.get('job', {})
                    comp = job.get('compensation', {}).get('inferredPay', {})
                    
                    #Handle date conversion
                    pub_date = job.get('datePublished')
                    formatted_date = 'Unknown'
                    if pub_date:
                        try:
                            # Assumes pub_date is in ms or a timestamp. adjust as needed
                            formatted_date = datetime.fromtimestamp(pub_date / 1000.0).strftime('%m/%d/%Y')
                        except: 
                            formatted_date = str(pub_date)
                            
                    jobs.append({
                        'jobTitle': job.get('title'),
                        'company': job.get('sourceEmployer'),
                        'location': job.get('location', {}).get('fullAddress'),
                        'salary': comp.get('basePay', 'Not listed'),
                        'jobUrl': f"https://www.indeed.com/viewjob?jk={job.get('key')}",
                        'postedDate': formatted_date
                    })
                    
            except Exception as e:
                print(f"Failed to parse internal JSON data: {e}")
                
        # 4. Fallback: Manual Selector Extraction (BeautifulSoup)
        if not jobs:
            for el in soup.select('.job_seen_beacon'):
                jobs.append({
                    'jobTitle': el.select_one('h2.jobTitle span').get_text(strip=True) if el.select_one('h2.jobTitle span') else el.select_one('h2.jobTitle').get_text(strip=True),
                    'company': el.select_one('[data-testid="company-name"]').get_text(strip=True) if el.select_one('.companyName') else 'N/A',
                    'location': el.select_one('[data-testid="text-location"]').get_text(strip=True) if el.select_one('[data-testid="text-location"]') else 'N/A',
                    'summary': el.select_one('.jobMetaDataGroup').get_text(strip=True) if el.select_one('.jobMetaDataGroup') else 'N/A',
                })
        return jobs
    
    def main():
        endpoint = os.getenv('EVOMI_ENDPOINT')
        api_key = os.getenv('API_KEY')
        
        payload = {
            'url': 'https://www.indeed.com/jobs?q=software+developer&l=New%20York%2C%20NY'
            # 'url': 'https://www.indeed.com/jobs?q=software+developer&l=Chicago%2C+IL'
            # 'url': 'https://www.indeed.com/jobs?q=software+developer&l=Las+Vegas'
        }
        
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            'referrer': "https://www.indeed.com/"
        }
            