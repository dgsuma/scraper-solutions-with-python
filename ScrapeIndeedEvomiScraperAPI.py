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