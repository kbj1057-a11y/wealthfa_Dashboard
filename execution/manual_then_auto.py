
import sys
import asyncio
import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

async def manual_login_then_automate():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [Step 1: Manual Login]")
    print("="*50)
    
    # Load news data
    news_file = Path(__file__).parent.parent / ".tmp" / "news_data.json"
    with open(news_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    news_list = news_data.get("insurance_news", [])
    
    print(f"\n Found {len(news_list)} news items ready to upload.")
    
    driver = None
    try:
        print("\n [1/5] Starting Chrome...")
        
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
        
        print(" [2/5] Opening NotebookLM...")
        notebook_url = "https://notebooklm.google.com/notebook/f097cbfd-b902-40a2-b309-a7c9c1a1d769"
        driver.get(notebook_url)
        
        print("\n" + "!"*50)
        print(" [ACTION REQUIRED]")
        print(" 1. Please LOG IN to Google in the browser window")
        print(" 2. Wait until you see the NOTEBOOK PAGE (not main page)")
        print(" 3. You should see the notebook title at the top")
        print(" 4. Then press [Enter] HERE in the terminal")
        print("!"*50)
        
        input("\nPress [Enter] when you're logged in and see the notebook...")
        
        print("\n [3/5] Thank you! Now I'll take over...")
        print(" Waiting for page to fully load...")
        await asyncio.sleep(5)
        
        print(" [4/5] Starting automated source addition...")
        
        for i, news in enumerate(news_list, 1):
            print(f"\n   [{i}/{len(news_list)}] Adding: {news['title'][:40]}...")
            
            try:
                # Click "Add source" button
                print("     > Clicking 'Add source'...")
                add_btn_script = """
                const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                const addBtn = btns.find(b => b.innerText.includes('노트북 만들기') || b.innerText.includes('Add source') || b.innerText.includes('소스 추가'));
                if(addBtn) { addBtn.click(); return true; }
                return false;
                """
                clicked = driver.execute_script(add_btn_script)
                if not clicked:
                    print("     > ERROR: Could not find 'Add source' button")
                    print("     > Please click it manually!")
                    await asyncio.sleep(10)
                
                await asyncio.sleep(3)
                
                # Click "Copied text"
                print("     > Selecting 'Copied text'...")
                text_script = """
                const opts = Array.from(document.querySelectorAll('div, span, button'));
                const textOpt = opts.find(o => o.innerText.includes('Copied text') || o.innerText.includes('복사한 텍스트') || o.innerText.includes('텍스트'));
                if(textOpt) { textOpt.click(); return true; }
                return false;
                """
                clicked = driver.execute_script(text_script)
                await asyncio.sleep(3)
                
                # Fill title
                print("     > Entering title...")
                title = f"InsuranceNews_{time.strftime('%m%d_%H%M')}_{i}"
                title_script = f"""
                const titleInput = document.querySelector('input[type="text"]');
                if(titleInput) {{
                    titleInput.value = '{title}';
                    titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return true;
                }}
                return false;
                """
                driver.execute_script(title_script)
                await asyncio.sleep(1)
                
                # Fill content
                print("     > Entering content...")
                content = f"Title: {news['title']}\\nMedia: {news['media']}\\nLink: {news['link']}\\n\\n{news['full_content'][:500]}"
                content = content.replace("'", "\\'").replace("\n", "\\n")
                content_script = f"""
                const area = document.querySelector('textarea');
                if(area) {{
                    area.value = `{content}`;
                    area.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return true;
                }}
                return false;
                """
                driver.execute_script(content_script)
                await asyncio.sleep(2)
                
                # Click Insert
                print("     > Clicking 'Insert'...")
                insert_script = """
                const btns = Array.from(document.querySelectorAll('button'));
                const insertBtn = btns.find(b => b.innerText.includes('Insert') || b.innerText.includes('추가') || b.innerText.includes('삽입'));
                if(insertBtn) { insertBtn.click(); return true; }
                return false;
                """
                clicked = driver.execute_script(insert_script)
                
                print(f"   [{i}/{len(news_list)}] Done!")
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"   [{i}/{len(news_list)}] ERROR: {str(e)}")
                await asyncio.sleep(3)
        
        print("\n [5/5] All sources added!")
        print("\n Please check the 'Sources' tab to verify.")
        print(" Browser will stay open for 2 minutes...")
        await asyncio.sleep(120)
        
    except KeyboardInterrupt:
        print("\n\n Interrupted.")
    except Exception as e:
        print(f"\n [ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\n Closing browser...")
            driver.quit()

if __name__ == "__main__":
    asyncio.run(manual_login_then_automate())
