import sys
import asyncio
import json
import time
from pathlib import Path
from utils import get_client, load_auth_data

async def upload_news_to_notebooklm():
    # Set standard output to UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("\n" + "="*50)
    print("      [Action: Knowledge Transplant] News Upload")
    print("="*50)
    
    # 1. 수집된 뉴스 데이터 로드
    news_file = Path(__file__).parent.parent / ".tmp" / "news_data.json"
    if not news_file.exists():
        print(" [ERROR] news_data.json not found in .tmp.")
        return

    with open(news_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    news_list = news_data.get("insurance_news", [])
    if not news_list:
        print(" [WARNING] News list is empty.")
        return

    print(f" [INFO] Found {len(news_list)} news items.")

    client = None
    try:
        # 2. 인증 및 클라이언트 시작
        auth_data = load_auth_data()
        client = get_client()
        
        print("\n [1/4] 브라우저 엔진 기동 중...")
        await client.start()
        
        # 3. 세션 주입
        print(" [2/4] 구글 인증 세션 주입 중...")
        client.driver.get("https://notebooklm.google.com")
        await asyncio.sleep(3)
        
        for cookie in auth_data.get('selenium_cookies', []):
            try:
                client.driver.add_cookie(cookie)
            except: pass
            
        client.driver.refresh()
        await asyncio.sleep(5)

        # 4. 타겟 노트북 진입
        notebook_id = "f097cbfd-b902-40a2-b309-a7c9c1a1d769"
        print(f" [3/4] Navigating to notebook: {notebook_id}...")
        await client.navigate_to_notebook(notebook_id)
        await asyncio.sleep(10) # 넉넉한 로딩 시간

        # 5. 뉴스 소스 추가 (초강력 JS 기반)
        print(f" [4/4] Starting JS-injected knowledge transplant...")
        
        js_find_and_click = """
        function findAndClick(textList) {
            const elements = document.querySelectorAll('button, div[role="button"], span');
            for (let el of elements) {
                if (textList.some(txt => el.innerText.includes(txt))) {
                    el.click();
                    return true;
                }
            }
            return false;
        }
        return findAndClick(arguments[0]);
        """

        for i, news in enumerate(news_list, 1):
            try:
                print(f"   - [{i}/{len(news_list)}] Processing: {news['title'][:20]}...")
                
                # 1) 'Add source' 클릭
                clicked = client.driver.execute_script(js_find_and_click, ["Add source", "소스 추가", "소스추가"])
                if not clicked:
                    # 사이드바가 닫혀있을 경우를 대비해 플러스 아이콘 등 탐색
                    client.driver.execute_script("document.querySelector('button[aria-label*=\"Add\"], button[aria-label*=\"추가\"]')?.click();")
                await asyncio.sleep(3)

                # 2) 'Copied text' 선택
                client.driver.execute_script(js_find_and_click, ["Copied text", "복사한 텍스트", "복사한텍스트"])
                await asyncio.sleep(3)

                # 3) 입력 (JS로 직접 값 주입)
                full_text = f"Title: {news['title']}\nMedia: {news['media']}\nLink: {news['link']}\n\nContent:\n{news['full_content']}"
                
                client.driver.execute_script("""
                    const title = document.querySelector('input[type="text"]');
                    if(title) {
                        title.value = arguments[0];
                        title.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    const area = document.querySelector('textarea, [contenteditable="true"]');
                    if(area) {
                        if(area.tagName === 'TEXTAREA') area.value = arguments[1];
                        else area.innerText = arguments[1];
                        area.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                """, f"InsuNews_{time.strftime('%m%d')}_{i}", full_text)
                await asyncio.sleep(2)

                # 4) 'Insert' 클릭
                client.driver.execute_script(js_find_and_click, ["Insert", "추가", "Add"])
                
                print(f"   - [{i}/{len(news_list)}] Success: {news['title'][:15]}...")
                await asyncio.sleep(5)

            except Exception as e:
                print(f"   - [{i}/{len(news_list)}] Failed.")
                client.driver.execute_script("document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));")
                await asyncio.sleep(2)

        print("\n" + "="*50)
        print(" [MISSION COMPLETE] JS-Powered Transplant Finished.")
        print(f" Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)

    except Exception as e:
        print(f"\n [CRITICAL ERROR] {str(e)}")
    finally:
        if client:
            print("\n Closing session after stabilization.")
            await asyncio.sleep(5)
            await client.close()

if __name__ == "__main__":
    asyncio.run(upload_news_to_notebooklm())
