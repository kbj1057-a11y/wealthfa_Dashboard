
import sys
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

async def open_notebook():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [Opening NotebookLM for Verification]")
    print("="*50)
    
    driver = None
    try:
        print("\n [1/2] Starting Chrome with saved profile...")
        
        opts = Options()
        
        # Use saved profile
        profile_dir = Path(__file__).parent.parent / ".chrome_profile"
        opts.add_argument(f"--user-data-dir={profile_dir.absolute()}")
        opts.add_argument("--profile-directory=Default")
        
        # Disable automation flags
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        
        # Enable cookies
        prefs = {
            "profile.default_content_setting_values.cookies": 1,
            "profile.block_third_party_cookies": False,
            "profile.cookie_controls_mode": 0,
        }
        opts.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=opts)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(" [2/2] Opening the notebook we just updated...")
        
        # Open the specific notebook
        notebook_url = "https://notebooklm.google.com/notebook/f097cbfd-b902-40a2-b309-a7c9c1a1d769"
        driver.get(notebook_url)
        
        await asyncio.sleep(5)
        
        print(f"\n [SUCCESS] Opened: {notebook_url}")
        print("\n Please check the 'Sources' section on the left.")
        print(" You should see the newly added news items:")
        print("   - InsuNews_0216_1")
        print("   - InsuNews_0216_2")
        print("\n Browser will stay open for 10 minutes.")
        print(" Press Ctrl+C to close earlier.")
        
        await asyncio.sleep(600)
        
    except KeyboardInterrupt:
        print("\n\n Closing browser...")
    except Exception as e:
        print(f"\n [ERROR] {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    asyncio.run(open_notebook())
