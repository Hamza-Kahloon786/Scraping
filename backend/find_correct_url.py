# Test script to find the correct ActuaryList URLs
import requests
from bs4 import BeautifulSoup

def find_actuarylist_urls():
    """Find the correct URLs for ActuaryList.com"""
    
    base_urls_to_try = [
        "https://www.actuarylist.com",
        "https://actuarylist.com", 
        "https://www.actuarylist.com/",
        "https://www.actuarylist.com/job-board",
        "https://www.actuarylist.com/careers",
        "https://www.actuarylist.com/job-search",
        "https://www.actuarylist.com/opportunities",
        "https://www.actuarylist.com/listings"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("🔍 Testing ActuaryList.com URLs...")
    print("=" * 60)
    
    working_urls = []
    
    for url in base_urls_to_try:
        try:
            print(f"\n📡 Testing: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                working_urls.append(url)
                
                # Parse the page to look for job-related content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Get page title
                title = soup.find('title')
                if title:
                    print(f"   Title: {title.get_text().strip()}")
                
                # Look for navigation links that might lead to jobs
                nav_links = soup.find_all('a', href=True)
                job_links = []
                
                for link in nav_links:
                    href = link.get('href', '').lower()
                    text = link.get_text().lower()
                    
                    if any(word in href or word in text for word in ['job', 'career', 'position', 'opportunity', 'listing']):
                        full_url = href if href.startswith('http') else f"https://www.actuarylist.com{href}"
                        job_links.append((text.strip(), full_url))
                
                if job_links:
                    print(f"   🎯 Found {len(job_links)} job-related links:")
                    for text, link in job_links[:5]:  # Show first 5
                        print(f"      '{text}' -> {link}")
                
                # Look for job-related keywords in the page
                page_text = response.text.lower()
                job_keywords = ['actuary', 'actuarial', 'insurance', 'job board', 'career']
                keyword_counts = {kw: page_text.count(kw) for kw in job_keywords}
                
                if any(count > 0 for count in keyword_counts.values()):
                    print(f"   📊 Job keywords found: {keyword_counts}")
                
            elif response.status_code == 404:
                print(f"   ❌ Not found (404)")
            elif response.status_code == 403:
                print(f"   🚫 Forbidden (403) - might be blocking scrapers")
            else:
                print(f"   ⚠️ Other status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📋 SUMMARY:")
    print(f"Working URLs: {len(working_urls)}")
    
    if working_urls:
        print(f"✅ SUCCESS: Found working URLs:")
        for url in working_urls:
            print(f"   {url}")
        
        # Test the main working URL for more details
        main_url = working_urls[0]
        print(f"\n🔍 Detailed analysis of: {main_url}")
        
        try:
            response = requests.get(main_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for forms that might be job search
            forms = soup.find_all('form')
            print(f"   Forms found: {len(forms)}")
            
            # Look for input fields
            inputs = soup.find_all('input')
            search_inputs = [inp for inp in inputs if any(word in str(inp).lower() 
                           for word in ['search', 'job', 'position', 'keyword'])]
            print(f"   Search inputs: {len(search_inputs)}")
            
            # Look for JavaScript frameworks
            scripts = soup.find_all('script')
            has_react = any('react' in str(script).lower() for script in scripts)
            has_vue = any('vue' in str(script).lower() for script in scripts)
            has_angular = any('angular' in str(script).lower() for script in scripts)
            
            print(f"   JavaScript frameworks:")
            print(f"      React: {has_react}")
            print(f"      Vue: {has_vue}")
            print(f"      Angular: {has_angular}")
            
            if has_react or has_vue or has_angular:
                print(f"   ⚠️ WARNING: Site uses JavaScript framework")
                print(f"      Simple HTTP scraping may not work")
                print(f"      Need Selenium for dynamic content")
            
        except Exception as e:
            print(f"   Error in detailed analysis: {e}")
    else:
        print(f"❌ FAILED: No working URLs found")
        print(f"   ActuaryList.com might be:")
        print(f"   - Down or unreachable")
        print(f"   - Blocking automated requests")
        print(f"   - Using a different domain")

if __name__ == "__main__":
    find_actuarylist_urls()