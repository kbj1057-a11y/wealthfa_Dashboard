
import sys
import asyncio
import time
from utils import get_client, load_auth_data

async def show_notebooklm_login():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [NotebookLM Login Demo]")
    print("="*50)
    
    client = None
    try:
        print("\n [1/3] Loading authentication...")
        auth_data = load_auth_data()
        
        print(" [2/3] Starting browser...")
        client = get_client()
        await client.start()
        
        print(" [3/3] Logging in to NotebookLM...")
        client.driver.get("https://notebooklm.google.com")
        await asyncio.sleep(3)
        
        # Inject cookies
        for cookie in auth_data.get('selenium_cookies', []):
            try:
                client.driver.add_cookie(cookie)
            except:
                pass
        
        # Refresh to apply cookies
        client.driver.refresh()
        await asyncio.sleep(5)
        
        current_url = client.driver.current_url
        print(f"\n [SUCCESS] Current URL: {current_url}")
        
        if "accounts.google.com" in current_url:
            print(" [WARNING] Redirected to login page - please log in manually")
            print("\n Please log in to Google in the browser window.")
            print(" After logging in, press Ctrl+C here to close the browser.")
        else:
            print(" [SUCCESS] Successfully logged in to NotebookLM!")
            print("\n Browser will stay open until you press Ctrl+C.")
            print(" You can now see your notebooks in the browser window.")
        
        # Keep browser open indefinitely
        print("\n Press Ctrl+C to close the browser...")
        await asyncio.sleep(3600)  # 1 hour max
        
    except Exception as e:
        print(f"\n [ERROR] {str(e)}")
    finally:
        if client:
            print("\n Closing browser...")
            await client.close()

if __name__ == "__main__":
    asyncio.run(show_notebooklm_login())
