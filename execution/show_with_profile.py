
import sys
import asyncio
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

async def show_with_profile():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [NotebookLM - Real Profile Login]")
    print("="*50)
    
    driver = None
    try:
        print("\n [1/2] Starting Chrome with your real profile...")
        
        opts = Options()
        
        # Use a dedicated profile for automation
        profile_dir = Path(__file__).parent.parent / ".chrome_profile"
        profile_dir.mkdir(exist_ok=True)
        
        opts.add_argument(f"--user-data-dir={profile_dir.absolute()}")
        opts.add_argument("--profile-directory=Default")
        
        # Disable automation flags
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        
        # Enable cookies explicitly
        prefs = {
            "profile.default_content_setting_values.cookies": 1,
            "profile.block_third_party_cookies": False,
            "profile.cookie_controls_mode": 0,
        }
        opts.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=opts)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(" [2/2] Opening NotebookLM...")
        driver.get("https://notebooklm.google.com")
        
        await asyncio.sleep(5)
        
        current_url = driver.current_url
        print(f"\n Current URL: {current_url}")
        
        if "accounts.google.com" in current_url:
            print("\n [INFO] Please log in manually in the browser.")
            print(" After logging in, the session will be saved automatically.")
        else:
            print("\n [SUCCESS] Already logged in!")
        
        print("\n Browser will stay open for 5 minutes.")
        print(" Press Ctrl+C to close earlier.")
        
        await asyncio.sleep(300)
        
    except KeyboardInterrupt:
        print("\n\n Closing browser...")
    except Exception as e:
        print(f"\n [ERROR] {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    asyncio.run(show_with_profile())
