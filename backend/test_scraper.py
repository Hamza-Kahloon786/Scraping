# Test script to check what ActuaryList.com actually returns
# Save this as test_scraper.py and run it to see what we get

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def test_actuarylist_scraping():
    """Test what we actually get from ActuaryList.com"""
    
    url = "https://www.actuarylist.com/jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"🔍 Testing scrape of: {url}")
    print("=" * 60)
    
    try:
        # Make request
        response = requests.get(url, headers=headers, timeout=30)
        print(f"📡 Response Status: {response.status_code}")
        print(f"📄 Response Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get page title
            title = soup.find('title')
            print(f"📋 Page Title: {title.get_text() if title else 'No title found'}")
            
            # Look for common job-related keywords in the HTML
            html_text = response.text.lower()
            keywords = ['actuary', 'actuarial', 'insurance', 'job', 'position', 'career']
            
            print(f"\n🔍 Keyword Analysis:")
            for keyword in keywords:
                count = html_text.count(keyword)
                print(f"   '{keyword}': {count} occurrences")
            
            # Try to find job listings with various selectors
            print(f"\n🎯 Job Element Search:")
            
            # Method 1: Look for common job listing classes
            job_classes = ['job', 'listing', 'card', 'item', 'position']
            for class_name in job_classes:
                elements = soup.find_all(['div', 'article'], class_=re.compile(class_name, re.I))
                print(f"   Class '{class_name}': {len(elements)} elements")
            
            # Method 2: Look for headings with job-like text
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
            job_headings = [h for h in headings if any(word in h.get_text().lower() 
                           for word in ['actuary', 'analyst', 'manager', 'director'])]
            print(f"   Job-like headings: {len(job_headings)}")
            
            # Method 3: Look for JavaScript/AJAX indicators
            scripts = soup.find_all('script')
            has_react = any('react' in str(script).lower() for script in scripts)
            has_ajax = any('ajax' in str(script).lower() for script in scripts)
            has_api = any('api' in str(script).lower() for script in scripts)
            
            print(f"\n⚙️ Technology Detection:")
            print(f"   React/SPA: {has_react}")
            print(f"   AJAX calls: {has_ajax}")
            print(f"   API calls: {has_api}")
            
            # Show first few job-like headings
            if job_headings:
                print(f"\n📝 Sample Job Headings Found:")
                for i, heading in enumerate(job_headings[:3]):
                    print(f"   {i+1}. {heading.get_text().strip()}")
            
            # Check if it's a single-page application
            if has_react or len(scripts) > 5:
                print(f"\n⚠️ LIKELY ISSUE: This appears to be a JavaScript-heavy site.")
                print(f"   Jobs are probably loaded dynamically via JavaScript.")
                print(f"   Simple HTML scraping won't work - need browser automation.")
            
            # Save a sample of the HTML for inspection
            sample_html = response.text[:2000]
            print(f"\n📄 HTML Sample (first 2000 chars):")
            print("-" * 40)
            print(sample_html)
            print("-" * 40)
            
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"❌ Response: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
    except Exception as e:
        print(f"❌ Other Error: {e}")

if __name__ == "__main__":
    test_actuarylist_scraping()