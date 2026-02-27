
import sys
import asyncio
import json
import time
from pathlib import Path
from utils import get_client, load_auth_data

async def create_new_transplant():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [Phase 2: Fresh Knowledge Base Creation]")
    print("="*50)
    
    news_file = Path(__file__).parent.parent / ".tmp" / "news_data.json"
    if not news_file.exists():
        print(" [ERROR] news_data.json not found.")
        return
    with open(news_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    news_list = news_data.get("insurance_news", [])

    client = None
    try:
        auth_data = load_auth_data()
        client = get_client()
        await client.start()
        
        client.driver.get("https://notebooklm.google.com")
        await asyncio.sleep(3)
        for cookie in auth_data.get('selenium_cookies', []):
            try: client.driver.add_cookie(cookie)
            except: pass
        client.driver.refresh()
        await asyncio.sleep(10)

        print(" [1/3] Creating a brand new notebook...")
        js_create = """
        const btn = Array.from(document.querySelectorAll('button, div[role="button"]'))
                     .find(el => el.innerText.includes('New notebook') || el.innerText.includes('새 노트북') || el.innerText.includes('+'));
        if(btn) btn.click();
        return !!btn;
        """
        client.driver.execute_script(js_create)
        await asyncio.sleep(15) 
        
        new_url = client.driver.current_url
        print(f" [2/3] New Notebook URL: {new_url}")

        print(f" [3/3] Transplanting {len(news_list)} items...")
        
        # UI-based loop with simple JS clicks
        for i, news in enumerate(news_list, 1):
            try:
                full_text = f"Title: {news['title']}\nMedia: {news['media']}\nLink: {news['link']}\n\n{news['full_content']}"
                title = f"Daily_Report_{time.strftime('%H%M')}_{i}"
                
                # Add source
                client.driver.execute_script("Array.from(document.querySelectorAll('button, span')).find(el => el.innerText.includes('Add source') || el.innerText.includes('소스 추가'))?.click();")
                await asyncio.sleep(3)
                
                # Copied text
                client.driver.execute_script("Array.from(document.querySelectorAll('div, span')).find(el => el.innerText.includes('Copied text') || el.innerText.includes('복사한 텍스트'))?.click();")
                await asyncio.sleep(3)
                
                # Fill data
                client.driver.execute_script("""
                    const title = document.querySelector('input[type="text"]');
                    const area = document.querySelector('textarea, [contenteditable="true"]');
                    if(title) { title.value = arguments[0]; title.dispatchEvent(new Event('input', { bubbles: true })); }
                    if(area) {
                        if(area.tagName === 'TEXTAREA') area.value = arguments[1];
                        else area.innerText = arguments[1];
                        area.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                """, title, full_text)
                await asyncio.sleep(2)
                
                # Insert
                client.driver.execute_script("Array.from(document.querySelectorAll('button')).find(el => el.innerText.includes('Insert') || el.innerText.includes('추가'))?.click();")
                print(f"   - Item {i} Success")
                await asyncio.sleep(5)
            except Exception as item_e:
                print(f"   - Item {i} Failed: {item_e}")

        print("\n" + "="*50)
        print(" [MISSION COMPLETE]")
        print(f" Final URL: {new_url}")
        print("="*50)

    except Exception as e:
        print(f" [ERROR] {str(e)}")
    finally:
        if client: await client.close()

if __name__ == "__main__":
    asyncio.run(create_new_transplant())
