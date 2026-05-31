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
    