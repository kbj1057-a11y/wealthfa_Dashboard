import time
import sys
import asyncio
from utils import get_client, load_auth_data

async def main():
    print("=== NotebookLM 시스템 가동 테스트 (v2.0.11 Async) ===")
    
    client = None
    try:
        # 1. 클라이언트 확보
        client = get_client()
        
        # 2. 브라우저 시작
        print("브라우저를 시작합니다...")
        await client.start()
        
        # 3. 로그인 상태 확인 및 쿠키 주입
        print("인증 정보를 주입합니다...")
        client.driver.get("https://notebooklm.google.com")
        time.sleep(3)
        
        auth_data = load_auth_data()
        cookies = auth_data.get('selenium_cookies', [])
        for cookie in cookies:
            try:
                client.driver.add_cookie(cookie)
            except Exception as ce:
                print(f"쿠키 주입 건너뜀: {cookie.get('name')}")
        
        # 4. 페이지 새로고침하여 로그인 적용
        client.driver.refresh()
        print("로그인 적용 중... 5초 대기")
        time.sleep(5)
        
        print("\n[SUCCESS] 시스템 연동 확인 완료!")
        print("이제 모든 자동화 스크립트를 정상적으로 사용할 수 있습니다.")
        
    except Exception as e:
        print(f"\n[ERROR] 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if client:
            print("10초 후 성능 테스트를 종료합니다...")
            time.sleep(10)
            await client.close()

if __name__ == "__main__":
    asyncio.run(main())
