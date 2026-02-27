import pyperclip
import time
import datetime
import pyautogui
from pywinauto import Application
import shutil
import os
import sys
import subprocess

# 한글 출력 깨짐 방지 및 버퍼링 해제
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# PyAutoGUI FAILSAFE 비활성화
pyautogui.FAILSAFE = False

# 실행 정보
XPLATFORM_PATH = r"C:\Program Files (x86)\TOBESOFT\XPLATFORM\9.1\XPlatform.exe"
XADL_URL = "https://www.samsunglifefs.kr/erp/xplatform/GMS/GMS.xadl"
USER_ID = "9495315"
USER_PW = "Qqudwls99**"

# 설정된 좌표 (사용자 측정 기반)
POS_CONTRACT_TOP = (451, 53)
POS_CONTRACT_SUB = (153, 344)
POS_START_DATE = (413, 163)
POS_SEARCH_BTN = (1127, 165)
POS_EXCEL_BTN = (1204, 165)
POS_REASON_INPUT = (452, 280)
POS_CONFIRM_BTN = (605, 511)

# 추가된 좌표
POS_LOGIN_ALREADY_OK = (967, 598)     # '이미 로그인되었습니다' 팝업 확인 버튼
POS_EXCEL_SAVE_CONFIRM = (-567, 566)  # 엑셀 저장 창의 '저장(S)' 버튼 (사용 안함)
POS_EXCEL_CLOSE_WIZARD = (1186, 757)  # 엑셀 인증 마법사 '닫기' 버튼

def save_excel_manually():
    """엑셀이 열린 상태에서 F12를 눌러 다른 이름으로 저장"""
    target_dir = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{now_str}_계약일자별조회.xlsx"
    full_path = os.path.join(target_dir, file_name)

    print(f"엑셀을 수동 저장합니다: {full_path}")
    
    # 0. 저장 전 엑셀 창이 확실히 활성화되도록 클릭 (화면 중앙)
    w, h = pyautogui.size()
    pyautogui.click(w//2, h//2)
    time.sleep(1)

    # 1. 경로 클립보드 복사
    pyperclip.copy(full_path)
    time.sleep(1)

    # 2. '다른 이름으로 저장' 단축키 (F12)
    print("F12 키 입력 (다른 이름으로 저장)")
    pyautogui.press('f12')
    time.sleep(3) # 저장 창 뜨는 시간 대기

    # 3. 파일 경로 붙여넣기
    print("파일 경로 붙여넣기 (Ctrl+V)")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    # 4. 저장 버튼 (Enter)
    print("저장 버튼 (Enter)")
    pyautogui.press('enter')
    time.sleep(2)

    # 5. 혹시 모를 '덮어쓰기 확인' 창 처리 (Y)
    print("덮어쓰기 확인 창 대비 (Y)")
    pyautogui.press('y') 
    time.sleep(1)

    # 6. 엑셀 종료 (Alt+F4)
    print("엑셀 종료 (Alt+F4)")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1.5)
    
    # 7. 종료 시 '저장하시겠습니까?' 팝업 처리 (Enter = 저장)
    print("종료 팝업 처리 (Enter)")
    pyautogui.press('enter')
    time.sleep(1)
    
    print(f"✅ 엑셀 저장 및 종료 완료: {file_name}")

def run_full_automation():
    try:
        # 1. 초기화 (기존 프로그램 종료)
        print("기존 프로그램을 종료하고 클린 부팅을 시작합니다...")
        os.system("taskkill /f /im XPlatform.exe /t")
        # os.system("taskkill /f /im EXCEL.EXE /t") # 사용자가 엑셀 종료 원하지 않음
        time.sleep(2)

        # 2. 프로그램 실행
        print("삼성생명 e-Partner 프로그램을 실행합니다...")
        subprocess.Popen([XPLATFORM_PATH, "-K", "e-Partner", "-X", XADL_URL])
        print("프로그램 로딩 대기 중 (15초)...")
        time.sleep(15) 
        
        # 3. 로그인 시도
        print("로그인 정보를 입력합니다...")
        # 창 활성화를 위해 화면 중앙 클릭
        w, h = pyautogui.size()
        pyautogui.click(w//2, h//2)
        time.sleep(2)
        
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(USER_ID)
        pyautogui.press('tab')
        pyautogui.write(USER_PW)
        pyautogui.press('enter')
        print("로그인 엔터를 눌렀습니다.")
        
        # 4. '이미 로그인되었습니다' 중복 로그인 팝업 처리
        print("중복 로그인 팝업 확인 대기 (3초)...")
        time.sleep(3)
        print(f"중복 로그인 확인 버튼 클릭: {POS_LOGIN_ALREADY_OK}")
        pyautogui.click(POS_LOGIN_ALREADY_OK)
        print("중복 로그인 확인 버튼 클릭 완료. (3초 대기)")
        time.sleep(3)
        
        print("로그인 완료 및 메인 화면 진입 대기 (10초)...")
        time.sleep(10)
        
        # 5. 계약 조회 프로세스
        print("계약 조회 메뉴로 진입합니다...")
        pyautogui.click(POS_CONTRACT_TOP)
        time.sleep(2)
        pyautogui.click(POS_CONTRACT_SUB)
        time.sleep(3)
        
        # 날짜 설정 (이번 달 1일)
        today = datetime.date.today()
        first_day = today.replace(day=1).strftime("%Y%m%d")
        print(f"날짜 설정: {first_day}")
        pyautogui.click(POS_START_DATE)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(first_day)
        pyautogui.press('enter')
        time.sleep(1)
        
        # 조회 버튼 클릭
        print("조회 버튼을 클릭합니다.")
        pyautogui.click(POS_SEARCH_BTN)
        time.sleep(7)
        
        # 6. 엑셀 다운로드 프로세스
        print("엑셀 다운로드를 시도합니다.")
        pyautogui.click(POS_EXCEL_BTN)
        time.sleep(3)
        
        # 사유 입력 'upmuyong' (업무용)
        pyautogui.click(POS_REASON_INPUT)
        time.sleep(1)
        pyautogui.write("upmuyong")
        time.sleep(1)
        pyautogui.click(POS_CONFIRM_BTN)
        print("다운로드 사유 입력 및 확인 완료.")
        
        # 7. 엑셀 저장 창 및 인증 마법사 처리
        print("엑셀 저장 창 대기 (5초)...")
        time.sleep(5)
        
        # 엑셀 인증 마법사 닫기
        print("엑셀 로딩 및 인증 마법사 대기 (10초)...")
        time.sleep(10)
        print(f"인증 마법사 닫기 클릭: {POS_EXCEL_CLOSE_WIZARD}")
        pyautogui.click(POS_EXCEL_CLOSE_WIZARD)
        print("인증 마법사 닫기 완료.")
        time.sleep(2)
        
        # 8. 수동 저장 (F12)
        save_excel_manually()
        
        print("\n\n🎉 [성공] 모든 자동화 업무가 완료되었습니다!")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    run_full_automation()
