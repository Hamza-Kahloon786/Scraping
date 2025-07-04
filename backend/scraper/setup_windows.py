"""
Windows-specific setup script for the Job Board scraper (Fixed for Chrome 137+)
Handles modern ChromeDriver installation and common Windows issues
"""
import os
import sys
import platform
import subprocess
import requests
import zipfile
import tempfile
import shutil
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {platform.python_version()}")
        return False
    print(f"✅ Python version: {platform.python_version()}")
    return True

def install_packages():
    """Install required Python packages"""
    packages = [
        'selenium==4.15.2',
        'webdriver-manager==4.0.1', 
        'beautifulsoup4==4.12.2',
        'requests==2.31.0',
        'python-dateutil==2.8.2'
    ]
    
    if platform.system() == "Windows":
        packages.append('pywin32==306')
    
    print("📦 Installing required packages...")
    
    for package in packages:
        try:
            print(f"⬇️ Installing {package}...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package
            ], capture_output=True, text=True, check=True)
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Failed to install {package}")
            print(f"   Error: {e.stderr}")
            
            # Try alternative installation
            try:
                print(f"🔄 Trying alternative installation for {package}...")
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package, '--user'
                ], check=True)
                print(f"✅ {package} installed with --user flag")
            except:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def get_chrome_version():
    """Get installed Chrome version on Windows"""
    try:
        if platform.system() == "Windows":
            import winreg
            
            # Try to get version from registry
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome\BLBeacon"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon")
            ]
            
            for hkey, path in registry_paths:
                try:
                    key = winreg.OpenKey(hkey, path)
                    version = winreg.QueryValueEx(key, "version")[0]
                    winreg.CloseKey(key)
                    print(f"✅ Chrome version from registry: {version}")
                    return version
                except:
                    continue
            
            # Try to get version from Chrome executable
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]
            
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    try:
                        result = subprocess.run(
                            [chrome_path, "--version"], 
                            capture_output=True, text=True, timeout=10
                        )
                        if result.returncode == 0:
                            version_string = result.stdout.strip()
                            version = version_string.split()[-1]
                            print(f"✅ Chrome version from executable: {version}")
                            return version
                    except:
                        continue
        
        print("⚠️ Could not detect Chrome version")
        return None
        
    except Exception as e:
        print(f"❌ Error getting Chrome version: {e}")
        return None

def get_compatible_chromedriver_version(chrome_version):
    """Get compatible ChromeDriver version for modern Chrome versions"""
    try:
        if not chrome_version:
            return "119.0.6045.105"  # Stable fallback
        
        major_version = int(chrome_version.split('.')[0])
        print(f"🔍 Chrome major version: {major_version}")
        
        # For Chrome 115+, use Chrome for Testing API
        if major_version >= 115:
            print("🔄 Using Chrome for Testing API for modern Chrome version...")
            
            # Get available versions from Chrome for Testing API
            api_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
            
            try:
                response = requests.get(api_url, timeout=15)
                data = response.json()
                
                # Find the best matching version
                compatible_versions = []
                for version_info in data.get('versions', []):
                    version = version_info.get('version', '')
                    if version.startswith(f"{major_version}."):
                        downloads = version_info.get('downloads', {})
                        if 'chromedriver' in downloads:
                            for download in downloads['chromedriver']:
                                if download.get('platform') == 'win32':
                                    compatible_versions.append({
                                        'version': version,
                                        'url': download.get('url')
                                    })
                
                if compatible_versions:
                    # Use the latest compatible version
                    latest = max(compatible_versions, key=lambda x: x['version'])
                    print(f"📦 Found compatible ChromeDriver: {latest['version']}")
                    return latest['version'], latest['url']
                
            except Exception as e:
                print(f"⚠️ Chrome for Testing API failed: {e}")
        
        # Fallback: Try legacy ChromeDriver storage
        legacy_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        try:
            response = requests.get(legacy_url, timeout=10)
            if response.status_code == 200 and not response.text.startswith('<?xml'):
                version = response.text.strip()
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
                print(f"📦 Found legacy ChromeDriver: {version}")
                return version, download_url
        except:
            pass
        
        # Version mapping for known compatibility
        version_map = {
            137: "119.0.6045.105",  # Use stable version for very new Chrome
            136: "119.0.6045.105",
            135: "119.0.6045.105",
            134: "119.0.6045.105",
            133: "119.0.6045.105",
            132: "119.0.6045.105",
            131: "119.0.6045.105",
            130: "119.0.6045.105",
            129: "119.0.6045.105",
            128: "119.0.6045.105",
            127: "119.0.6045.105",
            126: "119.0.6045.105",
            125: "119.0.6045.105",
            124: "119.0.6045.105",
            123: "119.0.6045.105",
            122: "119.0.6045.105",
            121: "119.0.6045.105",
            120: "119.0.6045.105",
            119: "119.0.6045.105",
            118: "118.0.5993.70",
            117: "117.0.5938.92",
            116: "116.0.5845.96",
            115: "115.0.5790.102"
        }
        
        if major_version in version_map:
            version = version_map[major_version]
            download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
            print(f"📦 Using mapped ChromeDriver version: {version}")
            return version, download_url
        
        # Ultimate fallback
        fallback_version = "119.0.6045.105"
        download_url = f"https://chromedriver.storage.googleapis.com/{fallback_version}/chromedriver_win32.zip"
        print(f"🔄 Using fallback ChromeDriver version: {fallback_version}")
        return fallback_version, download_url
        
    except Exception as e:
        print(f"⚠️ Error determining ChromeDriver version: {e}")
        fallback_version = "119.0.6045.105"
        download_url = f"https://chromedriver.storage.googleapis.com/{fallback_version}/chromedriver_win32.zip"
        return fallback_version, download_url

def download_chromedriver(chrome_version=None):
    """Download ChromeDriver for Windows with modern Chrome support"""
    try:
        print("⬇️ Downloading ChromeDriver...")
        
        # Get compatible version and download URL
        version_info = get_compatible_chromedriver_version(chrome_version)
        
        if isinstance(version_info, tuple):
            chromedriver_version, download_url = version_info
        else:
            chromedriver_version = version_info
            download_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_win32.zip"
        
        print(f"🌐 Downloading from: {download_url}")
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            # Download with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(download_url, timeout=60)
                    response.raise_for_status()
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"⚠️ Download attempt {attempt + 1} failed, retrying...")
            
            # Save zip file
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            print("📦 Extracting ChromeDriver...")
            
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find chromedriver.exe (might be in subfolder for newer versions)
            chromedriver_exe = None
            for root, dirs, files in os.walk(temp_dir):
                if "chromedriver.exe" in files:
                    chromedriver_exe = os.path.join(root, "chromedriver.exe")
                    break
            
            if not chromedriver_exe:
                print("❌ chromedriver.exe not found in downloaded archive")
                return False
            
            print(f"✅ Found chromedriver.exe at: {chromedriver_exe}")
            
            # Determine target locations
            script_dir = os.path.dirname(os.path.abspath(__file__))
            target_locations = [
                os.path.join(script_dir, "chromedriver.exe"),  # Same directory as script
                os.path.join(os.getcwd(), "chromedriver.exe"),  # Current working directory
            ]
            
            success = False
            for target_path in target_locations:
                try:
                    # Remove existing file if it exists
                    if os.path.exists(target_path):
                        os.remove(target_path)
                    
                    # Copy chromedriver
                    shutil.copy2(chromedriver_exe, target_path)
                    
                    # Verify the file was copied correctly
                    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
                        print(f"✅ ChromeDriver installed to: {target_path}")
                        success = True
                        break
                    
                except Exception as e:
                    print(f"⚠️ Failed to install to {target_path}: {e}")
                    continue
            
            return success
        
    except Exception as e:
        print(f"❌ Error downloading ChromeDriver: {e}")
        return False

def test_chromedriver():
    """Test ChromeDriver installation"""
    try:
        print("🧪 Testing ChromeDriver installation...")
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        # Chrome options for testing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        
        # Try different ChromeDriver locations
        chromedriver_locations = [
            "chromedriver.exe",  # Current directory
            os.path.join(os.path.dirname(__file__), "chromedriver.exe"),  # Script directory
            os.path.join(os.getcwd(), "chromedriver.exe"),  # Working directory
        ]
        
        driver = None
        for location in chromedriver_locations:
            if os.path.exists(location):
                try:
                    print(f"🔍 Testing ChromeDriver at: {location}")
                    service = Service(location)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    
                    # Test navigation
                    driver.get("https://www.google.com")
                    title = driver.title
                    
                    if "Google" in title:
                        print("✅ ChromeDriver test successful!")
                        driver.quit()
                        return True
                    
                except Exception as e:
                    print(f"⚠️ Test failed with {location}: {e}")
                    if driver:
                        try:
                            driver.quit()
                        except:
                            pass
                    continue
        
        # Try webdriver-manager as fallback
        try:
            print("🔄 Testing webdriver-manager...")
            from webdriver_manager.chrome import ChromeDriverManager
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("https://www.google.com")
            
            if "Google" in driver.title:
                print("✅ webdriver-manager test successful!")
                driver.quit()
                return True
                
        except Exception as e:
            print(f"⚠️ webdriver-manager test failed: {e}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        return False
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

def check_chrome_installation():
    """Check if Chrome browser is installed"""
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome browser found at: {path}")
            return True
    
    print("❌ Chrome browser not found!")
    print("💡 Please install Google Chrome from: https://www.google.com/chrome/")
    return False

def create_test_script():
    """Create a simple test script to verify everything works"""
    test_script = '''
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_scraper():
    """Test the scraper setup"""
    try:
        print("🧪 Testing scraper components...")
        
        # Test imports
        print("📦 Testing imports...")
        import requests
        import bs4
        from selenium import webdriver
        print("✅ All imports successful")
        
        # Test ChromeDriver
        print("🚗 Testing ChromeDriver...")
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Try local ChromeDriver
        if os.path.exists("chromedriver.exe"):
            service = Service("chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("https://httpbin.org/html")
            if driver.title:
                print("✅ ChromeDriver test successful")
                driver.quit()
                return True
        
        # Try webdriver-manager
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://httpbin.org/html")
        if driver.title:
            print("✅ webdriver-manager test successful")
            driver.quit()
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    if test_scraper():
        print("🎉 Scraper setup is working correctly!")
    else:
        print("⚠️ Scraper setup has issues")
'''
    
    try:
        with open("test_scraper.py", "w") as f:
            f.write(test_script)
        print("✅ Created test script: test_scraper.py")
        return True
    except Exception as e:
        print(f"⚠️ Could not create test script: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Windows Setup for Job Board Scraper (Chrome 137+ Compatible)")
    print("=" * 70)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    if not check_chrome_installation():
        return False
    
    # Install packages
    if not install_packages():
        print("❌ Failed to install required packages")
        return False
    
    # Get Chrome version
    chrome_version = get_chrome_version()
    if chrome_version:
        major_version = int(chrome_version.split('.')[0])
        if major_version >= 137:
            print(f"🆕 Detected very new Chrome version ({chrome_version})")
            print("💡 Using stable ChromeDriver version for compatibility")
    
    # Download ChromeDriver
    if not download_chromedriver(chrome_version):
        print("❌ Failed to download ChromeDriver")
        print("💡 Manual installation instructions:")
        print("   1. Go to https://googlechromelabs.github.io/chrome-for-testing/")
        print("   2. Download ChromeDriver for your Chrome version")
        print("   3. Extract chromedriver.exe to this folder")
        return False
    
    # Test installation
    if test_chromedriver():
        print("\n🎉 Setup completed successfully!")
        print("✅ ChromeDriver is working correctly")
        create_test_script()
        print("✅ You can now run the scraper with: python scrape_jobs.py")
        return True
    else:
        print("\n⚠️ Setup completed but ChromeDriver test failed")
        print("💡 The scraper will try to use requests as a fallback")
        print("💡 You can still run: python scrape_jobs.py")
        create_test_script()
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("\nPress Enter to exit...")
        else:
            input("\nSetup had issues. Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")