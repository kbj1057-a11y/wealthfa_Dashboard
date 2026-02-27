import time
import datetime
import pyautogui
from pywinauto import Application
import shutil
import os
import sys

# PyAutoGUI FAILSAFE 비활성화 (보안 프로그램 창 제어 시 구석으로 튐 방지)
pyautogui.FAILSAFE = False

# 설정된 좌표 (사용자 측정 기반)
POS_CONTRACT_TOP = (451, 53)       # 왼쪽 상단 '계약' 버튼
POS_CONTRACT_SUB = (153, 344)      # 왼쪽 '계약일자별' 메뉴
POS_START_DATE = (413, 163)        # 날짜 입력창(시작일)
POS_SEARCH_BTN = (1127, 165)        # 조회 버튼
POS_EXCEL_BTN = (1204, 165)         # 엑셀 다운로드 버튼
POS_REASON_INPUT = (452, 280)       # 다운로드 사유 입력창/선택창
POS_CONFIRM_BTN = (605, 511)        # 최종 확인/다운로드 버튼

def run_daily_task():
    try:
        print("삼성생명 e-Partner 업무 자동화를 시작합니다...")
        
        # 1. 창 활성화
        try:
            app = Application(backend="uia").connect(title="e-Partner", timeout=10)
            main_win = app.window(title="e-Partner")
            main_win.set_focus()
            print("e-Partner 창을 활성화했습니다.")
        except Exception as e:
            print(f"창 활성화 중 오류 (계속 진행 시도): {e}")
        
        time.sleep(1)
        
        # 2. '계약' 버튼 클릭
        print(f"'계약' 버튼 클릭 시도: {POS_CONTRACT_TOP}")
        pyautogui.click(POS_CONTRACT_TOP)
        time.sleep(1.5)
        
        # 3. '계약일자별' 메뉴 클릭
        print(f"'계약일자별' 메뉴 클릭 시도: {POS_CONTRACT_SUB}")
        pyautogui.click(POS_CONTRACT_SUB)
        time.sleep(2)
        
        # 4. 날짜 계산
        today = datetime.date.today()
        first_day = today.replace(day=1).strftime("%Y%m%d")
        print(f"조회 기간 설정: {first_day} ~ {today.strftime('%Y%m%d')}")
        
        # 5. 시작 날짜 입력
        print(f"시작 날짜 입력창 클릭 및 입력: {POS_START_DATE}")
        pyautogui.click(POS_START_DATE)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(first_day)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # 6. '조회' 버튼 클릭
        print(f"'조회' 버튼 클릭: {POS_SEARCH_BTN}")
        pyautogui.click(POS_SEARCH_BTN)
        print("데이터 조회 중... (3초 대기)")
        time.sleep(3)
        
        # 7. '엑셀 다운로드' 버튼 클릭
        print(f"'엑셀 다운로드' 버튼 클릭: {POS_EXCEL_BTN}")
        pyautogui.click(POS_EXCEL_BTN)
        time.sleep(2)
        
        # 8. 다운로드 사유 입력
        print(f"다운로드 사유 입력창 클릭: {POS_REASON_INPUT}")
        pyautogui.click(POS_REASON_INPUT)
        time.sleep(0.5)
        pyautogui.write("upmuyong") 
        time.sleep(0.5)
        
        # 9. 최종 확인 버튼 클릭
        print(f"최종 확인 버튼 클릭: {POS_CONFIRM_BTN}")
        pyautogui.click(POS_CONFIRM_BTN)
        
        # 10. 파일 이동 및 정리
        move_downloaded_file()
        
        print("\n[성공] 전 과정이 완료되었습니다.")
        
    except Exception as e:
        import traceback
        print(f"오류 상세 발생: {e}")
        traceback.print_exc()

def move_downloaded_file():
    download_dir = os.path.expanduser("~/Downloads")
    target_dir = "g:/내 드라이브/안티그래비티/TEST/계약관리(일자별)"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    print(f"파일 정리 중... (5초 대기)")
    time.sleep(5)
    
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
             if f.endswith(('.xlsx', '.xls', '.xlsb'))]
    
    if not files:
        print("최근 엑셀 파일을 찾지 못했습니다.")
        return
    
    latest_file = max(files, key=os.path.getmtime)
    file_name = os.path.basename(latest_file)
    
    today_str = datetime.date.today().strftime("%Y%m%d_%H%M%S")
    new_file_name = f"{today_str}_계약일자별조회_{file_name}"
    target_path = os.path.join(target_dir, new_file_name)
    
    try:
        shutil.move(latest_file, target_path)
        print(f"파일 이동 완료: {target_path}")
    except Exception as e:
        print(f"이동 중 오류: {e}")

if __name__ == "__main__":
    run_daily_task()
