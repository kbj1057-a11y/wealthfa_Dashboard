from pywinauto import Desktop
import time
import pyautogui

def find_actual_login_window():
    print("모든 활성 윈도우의 위치와 크기를 전수 조사합니다...")
    # uia와 win32 두 가지 백엔드 모두 확인 가능하지만 uia가 더 상세함
    windows = Desktop(backend="uia").windows()
    
    target_win = None
    
    for w in windows:
        try:
            title = w.window_text()
            rect = w.rectangle()
            width = rect.width()
            height = rect.height()
            
            # 너무 작지 않은 유효한 크기의 창들만 출력
            if width > 300 and height > 300:
                print(f"창 후보: [{title}] | 위치: ({rect.left}, {rect.top}) | 크기: {width}x{height}")
                
                # 'e-Partner'를 포함하거나, 제목이 없지만 크기가 로그인창 사이즈인 경우
                if "e-Partner" in title or "삼성" in title or title == "":
                    # 일반적으로 로그인 창은 화면 중앙 근처에 위치하거나 특정 크기(약 400~800)를 가짐
                    if 400 <= width <= 900 and 400 <= height <= 800:
                        print(f"  ==> 🎯 유력한 로그인 창 발견!")
                        target_win = w
        except:
            continue
            
    if target_win:
        print(f"\n최종 선택된 창: {target_win.window_text()}")
        target_win.set_focus()
        rect = target_win.rectangle()
        # 창의 중앙을 클릭하여 포커스 강제 확보
        cx, cy = rect.left + (rect.width()//2), rect.top + (rect.height()//2)
        print(f"중앙 클릭 시도: ({cx}, {cy})")
        pyautogui.click(cx, cy)
        time.sleep(1)
        
        # 확인을 위해 키보드 입력 테스트
        print("입력 테스트: 'TEST_ID' 입력 중...")
        pyautogui.write("TEST_ID")
        return True
    
    print("\n유효한 로그인 창을 특정하지 못했습니다.")
    return False

if __name__ == "__main__":
    find_actual_login_window()
