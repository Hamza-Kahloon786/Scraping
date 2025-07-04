"""
Selenium web scraper for actuarylist.com (Windows-compatible version)
Extracts job listings and saves them to the database
"""
import time
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import platform

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import requests

# Try to import webdriver-manager, fallback to manual setup
try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False
    print("⚠️ webdriver-manager not available, using manual ChromeDriver setup")

class ActuaryListScraper:
    """Scraper for actuarylist.com job listings with Windows compatibility"""
    
    def __init__(self, headless=True, max_jobs=50):
        self.base_url = "https://www.actuarylist.com"
        self.jobs_url = f"{self.base_url}/jobs"
        self.max_jobs = max_jobs
        self.headless = headless
        self.driver = None
        self.scraped_jobs = []
        
    def setup_driver(self):
        """Initialize the Chrome WebDriver with Windows compatibility"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Windows-specific Chrome options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")  # We'll enable if needed
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Disable logging
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Method 1: Try webdriver-manager
            if USE_WEBDRIVER_MANAGER:
                try:
                    print("🔄 Attempting to setup ChromeDriver using webdriver-manager...")
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    print("✅ ChromeDriver setup successful with webdriver-manager")
                    return True
                except Exception as e:
                    print(f"⚠️ webdriver-manager failed: {e}")
            
            # Method 2: Try system PATH
            try:
                print("🔄 Attempting to use ChromeDriver from system PATH...")
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✅ ChromeDriver setup successful from system PATH")
                return True
            except Exception as e:
                print(f"⚠️ System PATH ChromeDriver failed: {e}")
            
            # Method 3: Try manual ChromeDriver paths (Windows-specific)
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
                r"C:\Windows\System32\chromedriver.exe",
                r".\chromedriver.exe",
                r"..\chromedriver.exe",
                os.path.join(os.getcwd(), "chromedriver.exe")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        print(f"🔄 Trying ChromeDriver at: {path}")
                        service = Service(path)
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                        print(f"✅ ChromeDriver setup successful from: {path}")
                        return True
                    except Exception as e:
                        print(f"⚠️ Failed with {path}: {e}")
                        continue
            
            # Method 4: Download ChromeDriver manually
            print("🔄 Attempting to download ChromeDriver manually...")
            chromedriver_path = self.download_chromedriver()
            if chromedriver_path:
                try:
                    service = Service(chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    print("✅ ChromeDriver setup successful with manual download")
                    return True
                except Exception as e:
                    print(f"⚠️ Manual download failed: {e}")
            
            print("❌ All ChromeDriver setup methods failed")
            return False
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {e}")
            print(f"💡 Platform: {platform.system()} {platform.release()}")
            return False
    
    def download_chromedriver(self):
        """Download ChromeDriver manually for Windows"""
        try:
            import zipfile
            import tempfile
            
            # Get Chrome version
            chrome_version = self.get_chrome_version()
            if not chrome_version:
                print("❌ Could not detect Chrome version")
                return None
            
            print(f"🔍 Detected Chrome version: {chrome_version}")
            
            # ChromeDriver version URL
            version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version.split('.')[0]}"
            
            try:
                response = requests.get(version_url, timeout=10)
                chromedriver_version = response.text.strip()
                print(f"📦 ChromeDriver version: {chromedriver_version}")
            except:
                # Fallback to a stable version
                chromedriver_version = "119.0.6045.105"
                print(f"🔄 Using fallback ChromeDriver version: {chromedriver_version}")
            
            # Download ChromeDriver
            download_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_win32.zip"
            
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "chromedriver.zip")
                
                print(f"⬇️ Downloading ChromeDriver from: {download_url}")
                response = requests.get(download_url, timeout=30)
                response.raise_for_status()
                
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                # Extract ChromeDriver
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Move to current directory
                source_path = os.path.join(temp_dir, "chromedriver.exe")
                target_path = os.path.join(os.getcwd(), "chromedriver.exe")
                
                if os.path.exists(source_path):
                    if os.path.exists(target_path):
                        os.remove(target_path)
                    
                    import shutil
                    shutil.move(source_path, target_path)
                    print(f"✅ ChromeDriver downloaded to: {target_path}")
                    return target_path
                
            return None
            
        except Exception as e:
            print(f"❌ Error downloading ChromeDriver: {e}")
            return None
    
    def get_chrome_version(self):
        """Get installed Chrome version on Windows"""
        try:
            if platform.system() == "Windows":
                import winreg
                # Try to get version from registry
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                    version = winreg.QueryValueEx(key, "version")[0]
                    winreg.CloseKey(key)
                    return version
                except:
                    pass
                
                # Try alternative registry location
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome\BLBeacon")
                    version = winreg.QueryValueEx(key, "version")[0]
                    winreg.CloseKey(key)
                    return version
                except:
                    pass
                
                # Try to get version from Chrome executable
                import subprocess
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                ]
                
                for chrome_path in chrome_paths:
                    if os.path.exists(chrome_path):
                        try:
                            result = subprocess.run([chrome_path, "--version"], 
                                                  capture_output=True, text=True, timeout=10)
                            if result.returncode == 0:
                                version_string = result.stdout.strip()
                                version = version_string.split()[-1]
                                return version
                        except:
                            continue
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting Chrome version: {e}")
            return None
    
    def parse_posting_date(self, date_text: str) -> datetime:
        """Parse various date formats from the website"""
        if not date_text:
            return datetime.utcnow()
        
        date_text = date_text.strip().lower()
        now = datetime.utcnow()
        
        try:
            # Handle relative dates like "2 days ago", "1 week ago"
            if "day" in date_text:
                days_match = re.search(r'(\d+)\s*day', date_text)
                if days_match:
                    days = int(days_match.group(1))
                    return now - timedelta(days=days)
            
            elif "week" in date_text:
                weeks_match = re.search(r'(\d+)\s*week', date_text)
                if weeks_match:
                    weeks = int(weeks_match.group(1))
                    return now - timedelta(weeks=weeks)
            
            elif "hour" in date_text:
                hours_match = re.search(r'(\d+)\s*hour', date_text)
                if hours_match:
                    hours = int(hours_match.group(1))
                    return now - timedelta(hours=hours)
            
            elif "month" in date_text:
                months_match = re.search(r'(\d+)\s*month', date_text)
                if months_match:
                    months = int(months_match.group(1))
                    return now - timedelta(days=months * 30)  # Approximate
            
            # If it contains "today" or "yesterday"
            elif "today" in date_text:
                return now
            elif "yesterday" in date_text:
                return now - timedelta(days=1)
            
        except Exception as e:
            print(f"⚠️ Error parsing date '{date_text}': {e}")
        
        # Default to current time if parsing fails
        return now
    
    def scrape_with_requests(self) -> List[Dict]:
        """Fallback method using requests instead of Selenium"""
        print("🔄 Attempting to scrape using requests (fallback method)...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(self.jobs_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for job containers (this is a simplified approach)
            jobs = []
            job_count = 0
            
            # Try common job listing selectors
            job_selectors = [
                '.job-listing', '.job-item', '.job-card', '.job',
                '[class*="job"]', '.listing', '.position',
                'div[data-job]', 'article', '.vacancy'
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements
                    print(f"✅ Found {len(elements)} potential job elements using selector: {selector}")
                    break
            
            if not job_elements:
                # Try to find any divs that might contain job info
                job_elements = soup.find_all('div', limit=100)
                print(f"🔍 Found {len(job_elements)} div elements to analyze")
            
            for element in job_elements[:self.max_jobs]:
                try:
                    text = element.get_text(strip=True)
                    
                    # Skip if element is too small or too large
                    if len(text) < 20 or len(text) > 1000:
                        continue
                    
                    # Look for job-like content
                    if any(keyword in text.lower() for keyword in [
                        'actuary', 'actuarial', 'analyst', 'insurance', 
                        'job', 'position', 'career', 'full-time', 'part-time'
                    ]):
                        # Extract basic job information
                        job_info = self.extract_job_from_text(text, element)
                        if job_info:
                            jobs.append(job_info)
                            job_count += 1
                            print(f"✅ {job_count:2d}. {job_info.get('title', 'Unknown')} at {job_info.get('company', 'Unknown')}")
                            
                            if job_count >= self.max_jobs:
                                break
                
                except Exception as e:
                    continue
            
            return jobs
            
        except Exception as e:
            print(f"❌ Requests fallback failed: {e}")
            return []
    
    def extract_job_from_text(self, text: str, element) -> Optional[Dict]:
        """Extract job information from text content"""
        try:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if len(lines) < 2:
                return None
            
            # Assume first line is title, second is company
            title = lines[0]
            company = lines[1] if len(lines) > 1 else "Unknown Company"
            
            # Try to find location
            location = "Remote"
            for line in lines[2:5]:  # Check next few lines
                if any(keyword in line.lower() for keyword in [
                    'ny', 'ca', 'tx', 'fl', 'il', 'pa', 'oh', 'ga', 'nc', 'mi',
                    'new york', 'california', 'texas', 'florida', 'chicago',
                    'remote', 'hybrid', 'city', 'state', ','
                ]):
                    location = line
                    break
            
            # Determine job type
            job_type = "Full-time"
            text_lower = text.lower()
            if 'intern' in text_lower:
                job_type = "Internship"
            elif 'part-time' in text_lower or 'part time' in text_lower:
                job_type = "Part-time"
            elif 'contract' in text_lower:
                job_type = "Contract"
            
            # Extract tags
            tags = []
            actuarial_keywords = [
                'Life', 'Health', 'Property', 'Casualty', 'Pension',
                'Pricing', 'Reserving', 'Modeling', 'Valuation',
                'ASA', 'FSA', 'ACAS', 'FCAS', 'Python', 'R', 'SQL'
            ]
            
            for keyword in actuarial_keywords:
                if keyword.lower() in text_lower:
                    tags.append(keyword)
            
            # Get link if available
            source_url = self.jobs_url
            link_element = element.find('a', href=True)
            if link_element:
                href = link_element.get('href')
                if href:
                    if href.startswith('http'):
                        source_url = href
                    elif href.startswith('/'):
                        source_url = self.base_url + href
            
            return {
                'title': title[:200],  # Limit length
                'company': company[:200],
                'location': location[:200],
                'posting_date': datetime.utcnow(),
                'job_type': job_type,
                'tags': ', '.join(tags[:5]),
                'description': f"Job scraped from ActuaryList.com: {text[:300]}...",
                'source_url': source_url,
                'is_scraped': True
            }
            
        except Exception as e:
            return None
    
    def extract_job_info(self, job_element) -> Optional[Dict]:
        """Extract job information from a job listing element (Selenium version)"""
        try:
            job_data = {}
            
            # Get job title
            title_element = job_element.find_element(By.CSS_SELECTOR, "h3, .job-title, [class*='title']")
            job_data['title'] = title_element.text.strip() if title_element else "Unknown Title"
            
            # Get company name
            try:
                company_element = job_element.find_element(By.CSS_SELECTOR, ".company, [class*='company'], .employer")
                job_data['company'] = company_element.text.strip()
            except NoSuchElementException:
                job_data['company'] = "Unknown Company"
            
            # Get location
            try:
                location_element = job_element.find_element(By.CSS_SELECTOR, ".location, [class*='location'], .city")
                job_data['location'] = location_element.text.strip()
            except NoSuchElementException:
                job_data['location'] = "Remote"
            
            # Get posting date
            try:
                date_element = job_element.find_element(By.CSS_SELECTOR, ".date, [class*='date'], .posted, time")
                date_text = date_element.text.strip()
                job_data['posting_date'] = self.parse_posting_date(date_text)
            except NoSuchElementException:
                job_data['posting_date'] = datetime.utcnow()
            
            # Get job type (try to infer from title or description)
            job_type = "Full-time"  # Default
            title_lower = job_data['title'].lower()
            
            if any(word in title_lower for word in ['intern', 'internship']):
                job_type = "Internship"
            elif any(word in title_lower for word in ['part-time', 'part time']):
                job_type = "Part-time"
            elif any(word in title_lower for word in ['contract', 'contractor', 'consulting']):
                job_type = "Contract"
            
            job_data['job_type'] = job_type
            
            # Get tags/keywords
            tags = []
            try:
                # Look for tag elements
                tag_elements = job_element.find_elements(By.CSS_SELECTOR, ".tag, .skill, .keyword, [class*='tag'], [class*='skill']")
                for tag_elem in tag_elements:
                    tag_text = tag_elem.text.strip()
                    if tag_text and len(tag_text) < 50:  # Reasonable tag length
                        tags.append(tag_text)
            except:
                pass
            
            # Extract tags from title if no explicit tags found
            if not tags:
                # Common actuarial keywords
                actuarial_keywords = [
                    'Life', 'Health', 'Property', 'Casualty', 'Pension', 'Annuity',
                    'Pricing', 'Reserving', 'Modeling', 'Valuation', 'Risk', 'Analytics',
                    'Python', 'R', 'SQL', 'Excel', 'SAS', 'Prophet', 'AXIS',
                    'ASA', 'FSA', 'ACAS', 'FCAS', 'Actuary', 'Analyst', 'Senior', 'Junior'
                ]
                
                title_and_company = f"{job_data['title']} {job_data['company']}".lower()
                for keyword in actuarial_keywords:
                    if keyword.lower() in title_and_company:
                        tags.append(keyword)
            
            job_data['tags'] = ', '.join(tags[:5])  # Limit to 5 tags
            
            # Get source URL
            try:
                link_element = job_element.find_element(By.CSS_SELECTOR, "a[href]")
                href = link_element.get_attribute('href')
                if href and not href.startswith('http'):
                    href = self.base_url + href
                job_data['source_url'] = href
            except:
                job_data['source_url'] = self.jobs_url
            
            # Mark as scraped
            job_data['is_scraped'] = True
            job_data['description'] = f"Job scraped from ActuaryList.com"
            
            return job_data
            
        except Exception as e:
            print(f"⚠️ Error extracting job info: {e}")
            return None
    
    def scrape_jobs(self) -> List[Dict]:
        """Main scraping method with fallback options"""
        print(f"🚀 Starting to scrape jobs from {self.jobs_url}")
        print(f"🎯 Target: {self.max_jobs} jobs maximum")
        print(f"💻 Platform: {platform.system()} {platform.release()}")
        
        # Try Selenium first
        if self.setup_driver():
            try:
                return self.scrape_with_selenium()
            except Exception as e:
                print(f"⚠️ Selenium scraping failed: {e}")
                if self.driver:
                    self.driver.quit()
        
        # Fallback to requests
        print("🔄 Falling back to requests-based scraping...")
        return self.scrape_with_requests()
    
    def scrape_with_selenium(self) -> List[Dict]:
        """Scrape using Selenium WebDriver"""
        try:
            # Navigate to jobs page
            print("📄 Loading jobs page...")
            self.driver.get(self.jobs_url)
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, 10)
            
            # Handle potential cookie banner or popup
            try:
                # Common cookie banner selectors
                cookie_selectors = [
                    "button[id*='accept']",
                    "button[class*='accept']",
                    ".cookie-accept",
                    "#accept-cookies",
                    "[data-accept='true']"
                ]
                
                for selector in cookie_selectors:
                    try:
                        cookie_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if cookie_btn.is_displayed():
                            cookie_btn.click()
                            print("🍪 Accepted cookies")
                            time.sleep(1)
                            break
                    except:
                        continue
            except:
                pass
            
            # Look for job listings with various possible selectors
            job_selectors = [
                ".job-listing",
                ".job-item", 
                ".job-card",
                ".job",
                "[class*='job-']",
                ".listing",
                ".position"
            ]
            
            job_elements = []
            for selector in job_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        job_elements = elements
                        print(f"✅ Found {len(elements)} job elements using selector: {selector}")
                        break
                except:
                    continue
            
            if not job_elements:
                print("❌ No job elements found. Trying alternative approach...")
                # Try to find any elements that might contain job data
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Look for common patterns in job listings
                potential_jobs = soup.find_all(['div', 'article', 'section'], 
                                              class_=re.compile(r'job|listing|position|vacancy'))
                
                if potential_jobs:
                    print(f"🔍 Found {len(potential_jobs)} potential job containers with BeautifulSoup")
                    # Convert back to selenium elements for consistency
                    job_elements = self.driver.find_elements(By.XPATH, "//body//*")[:50]  # Limit search
                else:
                    print("❌ No job listings found on the page")
                    return []
            
            # Extract job information
            print(f"📊 Processing {min(len(job_elements), self.max_jobs)} job listings...")
            
            jobs_processed = 0
            for i, job_element in enumerate(job_elements[:self.max_jobs]):
                try:
                    job_info = self.extract_job_info(job_element)
                    
                    if job_info and job_info.get('title') and job_info.get('company'):
                        self.scraped_jobs.append(job_info)
                        jobs_processed += 1
                        
                        print(f"✅ {jobs_processed:2d}. {job_info['title']} at {job_info['company']}")
                        
                        # Small delay between extractions
                        time.sleep(0.5)
                    else:
                        print(f"⚠️ Skipped incomplete job listing {i+1}")
                        
                except Exception as e:
                    print(f"⚠️ Error processing job {i+1}: {e}")
                    continue
            
            print(f"🎉 Successfully scraped {len(self.scraped_jobs)} jobs!")
            return self.scraped_jobs
            
        except TimeoutException:
            print("❌ Timeout waiting for page to load")
            return []
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 WebDriver closed")

def save_jobs_to_database(jobs: List[Dict]) -> int:
    """Save scraped jobs to the database"""
    if not jobs:
        print("📭 No jobs to save")
        return 0
    
    try:
        from app import create_app
        from app.models import db, Job
        
        app = create_app()
        saved_count = 0
        skipped_count = 0
        
        with app.app_context():
            for job_data in jobs:
                try:
                    # Check for duplicates (same title + company)
                    existing_job = Job.query.filter_by(
                        title=job_data['title'],
                        company=job_data['company']
                    ).first()
                    
                    if existing_job:
                        skipped_count += 1
                        print(f"⏭️ Skipped duplicate: {job_data['title']} at {job_data['company']}")
                        continue
                    
                    # Create new job
                    job = Job(
                        title=job_data['title'],
                        company=job_data['company'],
                        location=job_data['location'],
                        posting_date=job_data['posting_date'],
                        job_type=job_data['job_type'],
                        tags=job_data['tags'],
                        description=job_data.get('description', ''),
                        source_url=job_data.get('source_url', ''),
                        is_scraped=True
                    )
                    
                    db.session.add(job)
                    saved_count += 1
                    
                except Exception as e:
                    print(f"⚠️ Error saving job '{job_data.get('title', 'Unknown')}': {e}")
                    continue
            
            # Commit all changes
            db.session.commit()
            
            print(f"💾 Database Results:")
            print(f"   ✅ Saved: {saved_count} new jobs")
            print(f"   ⏭️ Skipped: {skipped_count} duplicates")
            
            return saved_count
            
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        return 0

def install_requirements():
    """Install missing requirements"""
    try:
        import subprocess
        print("📦 Installing missing packages...")
        
        packages = ['requests', 'beautifulsoup4']
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                print(f"⬇️ Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        
        return True
    except Exception as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def main():
    """Main scraper execution"""
    print("🤖 ActuaryList.com Job Scraper (Windows Compatible)")
    print("=" * 50)
    
    # Check and install missing packages
    try:
        import requests
        import bs4
    except ImportError:
        print("📦 Missing required packages. Installing...")
        if not install_requirements():
            print("❌ Failed to install required packages")
            print("💡 Please run: pip install requests beautifulsoup4")
            return
        import requests
        import bs4
    
    # Print diagnostics
    print(f"🖥️ Platform: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    
    # Initialize scraper
    scraper = ActuaryListScraper(headless=True, max_jobs=50)
    
    # Scrape jobs
    jobs = scraper.scrape_jobs()
    
    if jobs:
        print(f"\n📊 Scraping Summary:")
        print(f"   🎯 Jobs found: {len(jobs)}")
        
        # Save to database
        print(f"\n💾 Saving jobs to database...")
        saved_count = save_jobs_to_database(jobs)
        
        print(f"\n🎉 Scraping completed!")
        print(f"   📥 Total jobs scraped: {len(jobs)}")
        print(f"   💾 Jobs saved to database: {saved_count}")
        
    else:
        print("❌ No jobs were scraped")
        print("\n🔧 Troubleshooting Tips:")
        print("1. Check your internet connection")
        print("2. Make sure Chrome browser is installed")
        print("3. Try running: pip install --upgrade selenium webdriver-manager")
        print("4. If Chrome issues persist, try installing ChromeDriver manually:")
        print("   - Download from: https://chromedriver.chromium.org/")
        print("   - Place chromedriver.exe in the same folder as this script")

if __name__ == "__main__":
    main()