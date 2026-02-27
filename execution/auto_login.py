import time
import sys
from pywinauto import Application, Desktop
import pyautogui

def auto_login(user_id, user_pw):
    try:
        print("e-Partner 자동 로그인을 시작합니다...")
        
        # 1. 창 찾기 및 포커스 설정
        # 윈도우 타이틀이 'e-Partner'인 창을 찾습니다.
        app = Application(backend="uia").connect(title="e-Partner", timeout=10)
        main_win = app.window(title="e-Partner")
        
        print("프로그램 창을 활성화합니다.")
        main_win.set_focus()
        time.sleep(1) # 활성화 대기
        
        # 2. 로그인 입력 (ID -> Tab -> PW -> Enter)
        print(f"ID 입력을 시도합니다...")
        # 기존 내용 삭제를 위해 Ctrl+A 후 Backspace (안전장치)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        
        # ID 타이핑
        pyautogui.write(user_id)
        time.sleep(0.5)
        
        # PW 창으로 이동
        print("PW 창으로 이동 (Tab)...")
        pyautogui.press('tab')
        time.sleep(0.5)
        
        # PW 타이핑
        print("PW 입력을 시도합니다...")
        pyautogui.write(user_pw)
        time.sleep(0.5)
        
        # 로그인 실행
        print("로그인 실행 (Enter)...")
        pyautogui.press('enter')
        
        print("로그인 명령 전송 완료. 결과를 확인해 주세요.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print("프로그램 창을 찾을 수 없거나 활성화에 실패했습니다.")

if __name__ == "__main__":
    # 테스트를 위한 구문 (실제 실행 시에는 ID/PW를 인자로 넘기도록 설계)
    if len(sys.argv) < 3:
        print("사용법: python auto_login.py <ID> <PW>")
    else:
        auto_login(sys.argv[1], sys.argv[2])
