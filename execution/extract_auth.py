import json
import time
import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_notebooklm_auth():
    # Set standard output to UTF-8 to prevent cp949 errors if possible
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      NotebookLM Auth Extraction System")
    print("="*50)
    
    chrome_options = Options()
    # Ensure a clean session for authentication
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("\n[1/3] Launching Secure Chrome instance...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("[2/3] Navigating to NotebookLM...")
        driver.get("https://notebooklm.google.com")
        
        print("\n" + "!"*50)
        print(" [ACTION REQUIRED] ")
        print(" 1. Please log in to your Google Account.")
        print(" 2. Navigate until you see your personal notebooks.")
        print(" 3. DON'T touch the browser once you are on the dashboard.")
        print("!"*50)
        
        input("\nPress [Enter] HERE once login is complete and you see your notebooks...")
        
        print("\n[3/3] Extracting credentials and system tokens...")
        
        # Give it time to load data
        time.sleep(5)
        
        cookies = driver.get_cookies()
        if not cookies:
            print(" WARNING: No cookies found. Ensure you are logged in.")
            cookies = []

        cookie_dict = {c.get('name'): c.get('value') for c in cookies if isinstance(c, dict)}
        
        csrf_token = None
        
        # Method 1: Global Variables
        scripts = [
            "return (window.WIZ_global_data && window.WIZ_global_data.at) || null;",
            "return (window._SN_config && window._SN_config[1]) || null;"
        ]
        
        for s in scripts:
            try:
                res = driver.execute_script(s)
                if res and isinstance(res, str) and len(res) > 20:
                    csrf_token = res
                    break
            except: pass
            
        # Method 2: Regex in page source
        if not csrf_token:
            try:
                import re
                page_source = driver.page_source
                match = re.search(r'\"at\":\"(.*?)\"', page_source)
                if match:
                    csrf_token = match.group(1)
            except: pass

        # FINAL FALLBACK: Interactive Manual Entry while browser is still open
        if not csrf_token:
            print("\n" + "!"*50)
            print(" 🛑 AUTOMATIC EXTRACTION FAILED")
            print(" 1. Go to the opened browser window.")
            print(" 2. Press F12 -> Console.")
            print(" 3. Type: window.WIZ_global_data.at")
            print(" 4. Copy the long string (e.g., 'AFpdq...') and paste it here.")
            print("!"*50)
            manual_token = input("\nPASTE CSRF TOKEN HERE (or press Enter to skip): ").strip()
            if manual_token:
                csrf_token = manual_token

        auth_data = {
            "cookies": cookie_dict,
            "csrf_token": csrf_token or "MANUAL_INPUT_REQUIRED",
            "session_id": cookie_dict.get('SID', "NOT_FOUND"),
            "extracted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "SUCCESS" if csrf_token and len(csrf_token) > 20 else "PARTIAL_SUCCESS"
        }
        
        project_root = Path(__file__).parent.parent
        auth_file = project_root / "auth.json"
        
        with open(auth_file, 'w', encoding='utf-8') as f:
            json.dump(auth_data, f, indent=2, ensure_ascii=False)
            
        print("\n" + "="*50)
        if auth_data["status"] == "SUCCESS":
            print(f" SUCCESS: Credentials saved to {auth_file}")
            print(f" CSRF Token: {str(csrf_token)[:15]}... (Locked & Loaded)")
        else:
            print(f" WARNING: Saved but CSRF is still missing. Automatic tools will fail.")
        print("="*50)
        
    except Exception as e:
        print(f"\n ERROR: {str(e)}")
    finally:
        if driver:
            print("\nShutting down browser in 3 seconds...")
            time.sleep(3)
            driver.quit()

if __name__ == "__main__":
    extract_notebooklm_auth()
