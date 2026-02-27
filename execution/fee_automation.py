
import sys
import os
import time
import datetime
import subprocess
import pyperclip
import pyautogui
from pywinauto import Desktop

# 한글 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# PyAutoGUI 설정
pyautogui.FAILSAFE = False

# ==========================================
# 📍 좌표 설정 (사용자 업데이트 완료: 2026-02-19)
# ==========================================
# 0. 공통/로그인
XPLATFORM_PATH = r"C:\Program Files (x86)\TOBESOFT\XPLATFORM\9.1\XPlatform.exe"
XADL_URL = "https://www.samsunglifefs.kr/erp/xplatform/GMS/GMS.xadl"
USER_ID = "9495315"
USER_PW = "Qqudwls99**"
POS_LOGIN_ALREADY_OK = (967, 598)     # 중복 로그인 팝업 '확인'

# 1. 메뉴 이동
POS_MENU_FEE_AFC = (754, 59)             # 수수료_AFC
POS_SUBMENU_EXPECTED_FEE = (128, 230)     # 예상수수료조회_AFC

# 2. 조회 옵션 설정 (2단계 클릭)
POS_RADIO_LIFE_L1_STEP1 = (755, 212)      # 수수료레벨 생보L1 (1차)
POS_RADIO_LIFE_L1_STEP2 = (730, 276)      # 수수료레벨 생보L1 (2차 - 확인/선택)

POS_RADIO_NONLIFE_L2_STEP1 = (852, 216)   # 수수료레벨 손보L2 (1차)
POS_RADIO_NONLIFE_L2_STEP2 = (841, 299)   # 수수료레벨 손보L2 (2차 - 확인/선택)

POS_BTN_INQUIRY = (1129, 169)              # 조회 버튼

# 3. 엑셀 다운로드
POS_BTN_EXCEL = (1198, 167)                # 엑셀 다운로드 버튼
POS_EXCEL_REASON_INPUT = (452, 280)   # 사유 입력창 (기존값 유지/필요시 갱신)
POS_EXCEL_CONFIRM_BTN = (605, 511)    # 사유 입력 확인 (기존값 유지/필요시 갱신)
POS_EXCEL_CLOSE_WIZARD = (1186, 757)  # 엑셀 마법사 닫기 (기존값 유지/필요시 갱신)

# ==========================================

def clean_start():
    """기존 프로세스 종료"""
    print("🔄 [초기화] 기존 XPlatform 종료 중...")
    os.system("taskkill /f /im XPlatform.exe /t >nul 2>&1")
    time.sleep(2)

def launch_application():
    """애플리케이션 실행"""
    print("🚀 [실행] e-Partner 실행...")
    subprocess.Popen([XPLATFORM_PATH, "-K", "e-Partner", "-X", XADL_URL])
    
    # 창이 뜰 때까지 대기 (최대 30초)
    print("⏳ [대기] 프로그램 로딩 대기 중...")
    for i in range(30):
        if find_target_window():
            print(f"✅ [감지] 프로그램 창이 감지되었습니다. ({i+1}초 소요)")
            time.sleep(5)  # UI 렌더링 안정화 대기
            return True
        time.sleep(1)
    
    print("❌ [실패] 프로그램이 실행되지 않았거나 창을 찾을 수 없습니다.")
    return False

def find_target_window():
    """타겟 윈도우 존재 확인"""
    try:
        windows = Desktop(backend="uia").windows()
        for w in windows:
            if "e-Partner" in w.window_text() or "삼성생명" in w.window_text():
                return w
    except:
        pass
    return None

def login_process():
    """로그인 수행"""
    print("🔑 [로그인] ID/PW 입력 시도...")
    
    w, h = pyautogui.size()
    pyautogui.click(w//2, h//2)
    time.sleep(1)

    # ID
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(USER_ID)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # PW
    pyautogui.press('tab')
    pyperclip.copy(USER_PW)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    pyautogui.press('enter')
    print("✅ [입력] 로그인 정보 제출 완료.")

def handle_popups():
    """중복 로그인 등 팝업 처리"""
    print("🛡️ [팝업] 팝업 창 대기 (3초)...")
    time.sleep(3)
    pyautogui.click(POS_LOGIN_ALREADY_OK)
    print("✅ [클릭] 팝업 확인 버튼 클릭 (예상).")

def navigate_menu():
    """메뉴 이동 및 조회 옵션 설정"""
    print("\n📂 [메뉴] '수수료_AFC' 이동 중...")
    pyautogui.click(POS_MENU_FEE_AFC)
    time.sleep(2)
    
    print("📂 [메뉴] '예상수수료조회_AFC' 클릭...")
    pyautogui.click(POS_SUBMENU_EXPECTED_FEE)
    time.sleep(5) # 화면 로딩 대기
    
    # 생보L1 설정 (2단계)
    print("⚙️ [설정] '수수료레벨 생보L1' 설정 (1단계)...")
    pyautogui.click(POS_RADIO_LIFE_L1_STEP1)
    time.sleep(0.5)
    print("⚙️ [설정] '수수료레벨 생보L1' 설정 (2단계)...")
    pyautogui.click(POS_RADIO_LIFE_L1_STEP2)
    time.sleep(1)

    # 손보L2 설정 (2단계)
    print("⚙️ [설정] '수수료레벨 손보L2' 설정 (1단계)...")
    pyautogui.click(POS_RADIO_NONLIFE_L2_STEP1)
    time.sleep(0.5)
    print("⚙️ [설정] '수수료레벨 손보L2' 설정 (2단계)...")
    pyautogui.click(POS_RADIO_NONLIFE_L2_STEP2)
    time.sleep(1)
    
    print("🔍 [조회] 조회 버튼 클릭...")
    pyautogui.click(POS_BTN_INQUIRY)
    print("⏳ [대기] 조회 결과 대기 (10초)...")
    time.sleep(10)
    
    return True

def save_excel_process():
    """엑셀 다운로드 및 저장"""
    print("\n💾 [엑셀] 다운로드 시작...")
    pyautogui.click(POS_BTN_EXCEL)
    time.sleep(3)
    
    # 사유 입력
    print("✍️ [입력] 다운로드 사유 입력...")
    pyautogui.click(POS_EXCEL_REASON_INPUT)
    time.sleep(1)
    pyautogui.write("upmuyong") # 업무용
    time.sleep(1)
    pyautogui.click(POS_EXCEL_CONFIRM_BTN)
    
    print("⏳ [대기] 엑셀 뷰어 실행 대기 (15초)...")
    time.sleep(15)
    
    # 인증 마법사 닫기
    print("❌ [닫기] 엑셀 인증 마법사 닫기...")
    pyautogui.click(POS_EXCEL_CLOSE_WIZARD)
    time.sleep(2)
    
    # 파일명 생성
    target_dir = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
    os.makedirs(target_dir, exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(target_dir, f"{today_str}_예상수수료.xlsx")
    
    # 다른 이름으로 저장 (F12)
    print(f"💾 [저장] 엑셀 저장 시도: {file_path}")
    pyautogui.press('f12')
    time.sleep(3)
    
    pyperclip.copy(file_path)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter') # 저장
    time.sleep(2)
    
    pyautogui.press('y') # 덮어쓰기 확인
    time.sleep(1)
    
    # 종료
    print("👋 [종료] 엑셀 닫기...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.press('enter') # 저장 여부 팝업 엔터
    
    print("✅ [완료] 모든 작업이 마무리되었습니다.")

def main():
    print("======== e-Partner 예상수수료 자동화 ========", flush=True)
    
    # 1. 로그인
    clean_start()
    if not launch_application():
        return
        
    login_process()
    handle_popups()
    
    print("\n메인 화면 진입 대기 (10초)...")
    time.sleep(10)
    
    # 2. 메뉴 이동 및 조회
    if navigate_menu():
        # 3. 엑셀 다운로드
        save_excel_process()
    else:
        print("\n⚠️ [안내] 좌표가 설정되지 않아 작업을 중단합니다.")
        print("`execution/track_mouse.py`를 실행하여 좌표를 확인한 후 코드를 업데이트해주세요.")

if __name__ == "__main__":
    main()

