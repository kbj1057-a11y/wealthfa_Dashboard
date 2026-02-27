from pywinauto import Desktop
import time

def find_samsung_windows():
    print("현재 실행 중인 윈도우 목록을 검색합니다...")
    windows = Desktop(backend="uia").windows()
    found = False
    for w in windows:
        title = w.window_text()
        if title:
            print(f"창 발견: {title}")
            if "삼성생명" in title or "e-Partner" in title or "XPLATFORM" in title:
                print(f"==> 타겟 창 매칭 성공: {title}")
                found = True
    
    if not found:
        print("삼성생명 관련 창을 찾지 못했습니다. 프로그램을 실행 중인지 확인해 주세요.")

if __name__ == "__main__":
    find_samsung_windows()
