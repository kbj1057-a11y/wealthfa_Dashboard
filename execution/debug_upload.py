
import sys
import asyncio
import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def manual_upload_demo():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [Live Demo: Adding Sources to NotebookLM]")
    print("="*50)
    
    # Load news data
    news_file = Path(__file__).parent.parent / ".tmp" / "news_data.json"
    with open(news_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    news_list = news_data.get("insurance_news", [])
    
    print(f"\n Found {len(news_list)} news items to upload.")
    
    driver = None
    try:
        print("\n [1/4] Starting Chrome with saved profile...")
        
        opts = Options()
        profile_dir = Path(__file__).parent.parent / ".chrome_profile"
        opts.add_argument(f"--user-data-dir={profile_dir.absolute()}")
        opts.add_argument("--profile-directory=Default")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        
        prefs = {
            "profile.default_content_setting_values.cookies": 1,
            "profile.block_third_party_cookies": False,
            "profile.cookie_controls_mode": 0,
        }
        opts.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=opts)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(" [2/4] Opening notebook...")
        notebook_url = "https://notebooklm.google.com/notebook/f097cbfd-b902-40a2-b309-a7c9c1a1d769"
        driver.get(notebook_url)
        await asyncio.sleep(8)
        
        print(" [3/4] Starting manual source addition...")
        print("\n WATCH THE BROWSER - You'll see automation in action!")
        
        for i, news in enumerate(news_list, 1):
            print(f"\n   [{i}/{len(news_list)}] Processing: {news['title'][:30]}...")
            
            try:
                # Step 1: Find and click "Add source" button
                print("     > Looking for 'Add source' button...")
                await asyncio.sleep(2)
                
                # Try multiple selectors
                add_source_clicked = False
                selectors = [
                    "//button[contains(., 'Add source')]",
                    "//button[contains(., '소스 추가')]",
                    "//button[contains(@aria-label, 'Add')]",
                    "//div[@role='button'][contains(., 'Add')]"
                ]
                
                for selector in selectors:
                    try:
                        btn = driver.find_element(By.XPATH, selector)
                        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                        await asyncio.sleep(1)
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"     > Clicked 'Add source' button (selector: {selector[:30]}...)")
                        add_source_clicked = True
                        break
                    except:
                        continue
                
                if not add_source_clicked:
                    print("     > ERROR: Could not find 'Add source' button")
                    print("     > Please click 'Add source' button manually now!")
                    await asyncio.sleep(10)
                
                await asyncio.sleep(3)
                
                # Step 2: Click "Copied text" option
                print("     > Looking for 'Copied text' option...")
                text_clicked = False
                text_selectors = [
                    "//div[contains(text(), 'Copied text')]",
                    "//div[contains(text(), '복사한 텍스트')]",
                    "//button[contains(., 'text')]"
                ]
                
                for selector in text_selectors:
                    try:
                        opt = driver.find_element(By.XPATH, selector)
                        driver.execute_script("arguments[0].click();", opt)
                        print(f"     > Clicked 'Copied text' option")
                        text_clicked = True
                        break
                    except:
                        continue
                
                if not text_clicked:
                    print("     > ERROR: Could not find 'Copied text' option")
                    await asyncio.sleep(5)
                
                await asyncio.sleep(3)
                
                # Step 3: Fill in title and content
                print("     > Filling in title and content...")
                title = f"News_{time.strftime('%H%M')}_{i}"
                content = f"Title: {news['title']}\nMedia: {news['media']}\nLink: {news['link']}\n\n{news['full_content']}"
                
                # Find input fields
                try:
                    title_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
                    title_input.clear()
                    title_input.send_keys(title)
                    print(f"     > Title entered: {title}")
                except Exception as e:
                    print(f"     > ERROR finding title input: {e}")
                
                await asyncio.sleep(1)
                
                try:
                    content_area = driver.find_element(By.TAG_NAME, "textarea")
                    content_area.clear()
                    content_area.send_keys(content[:500])  # Limit to 500 chars for demo
                    print(f"     > Content entered (first 500 chars)")
                except Exception as e:
                    print(f"     > ERROR finding content area: {e}")
                
                await asyncio.sleep(2)
                
                # Step 4: Click Insert/Add button
                print("     > Looking for 'Insert' button...")
                insert_clicked = False
                insert_selectors = [
                    "//button[contains(., 'Insert')]",
                    "//button[contains(., '추가')]",
                    "//button[contains(., 'Add')]"
                ]
                
                for selector in insert_selectors:
                    try:
                        btn = driver.find_element(By.XPATH, selector)
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"     > Clicked 'Insert' button")
                        insert_clicked = True
                        break
                    except:
                        continue
                
                if not insert_clicked:
                    print("     > ERROR: Could not find 'Insert' button")
                
                print(f"   [{i}/{len(news_list)}] Completed!")
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"   [{i}/{len(news_list)}] ERROR: {str(e)}")
                await asyncio.sleep(3)
        
        print("\n [4/4] All done! Check the notebook for sources.")
        print("\n Browser will stay open for 2 minutes for verification.")
        await asyncio.sleep(120)
        
    except KeyboardInterrupt:
        print("\n\n Interrupted by user.")
    except Exception as e:
        print(f"\n [ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\n Closing browser...")
            driver.quit()

if __name__ == "__main__":
    asyncio.run(manual_upload_demo())
