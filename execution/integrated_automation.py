
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
# 📍 통합 좌표 설정 (사용자 업데이트 완료)
# ==========================================
# 0. 공통/로그인
XPLATFORM_PATH = r"C:\Program Files (x86)\TOBESOFT\XPLATFORM\9.1\XPlatform.exe"
XADL_URL = "https://www.samsunglifefs.kr/erp/xplatform/GMS/GMS.xadl"
USER_ID = "9495315"
USER_PW = "Qqudwls99**"
POS_LOGIN_ALREADY_OK = (967, 598)     # 중복 로그인 팝업 '확인'

# 1-1. 계약관리 메뉴
POS_CONTRACT_TOP = (451, 53)
POS_CONTRACT_SUB = (153, 344)
POS_START_DATE = (413, 163)
POS_SEARCH_BTN = (1127, 165)
POS_EXCEL_BTN = (1204, 165)
POS_REASON_INPUT = (452, 280)
POS_CONFIRM_BTN = (605, 511)
POS_EXCEL_CLOSE_WIZARD = (1186, 757)

# 1-2. 수수료관리 메뉴
POS_MENU_FEE_AFC = (754, 59)             # 수수료_AFC
POS_SUBMENU_EXPECTED_FEE = (128, 230)     # 예상수수료조회_AFC

POS_RADIO_LIFE_L1_STEP1 = (755, 212)      # 수수료레벨 생보L1 (1차)
POS_RADIO_LIFE_L1_STEP2 = (730, 276)      # 수수료레벨 생보L1 (2차 - 확인/선택)
POS_RADIO_NONLIFE_L2_STEP1 = (852, 216)   # 수수료레벨 손보L2 (1차)
POS_RADIO_NONLIFE_L2_STEP2 = (841, 299)   # 수수료레벨 손보L2 (2차 - 확인/선택)

POS_Btn_INQUIRY_FEE = (1129, 169)         # 조회 버튼 (수수료)
POS_Btn_EXCEL_FEE = (1198, 167)           # 엑셀 다운로드 버튼 (수수료)

# ==========================================

def clean_start():
    print("🔄 [초기화] 기존 XPlatform 종료 중...")
    os.system("taskkill /f /im XPlatform.exe /t >nul 2>&1")
    time.sleep(2)

def launch_application():
    print("🚀 [실행] e-Partner 실행...")
    subprocess.Popen([XPLATFORM_PATH, "-K", "e-Partner", "-X", XADL_URL])
    
    print("⏳ [대기] 프로그램 로딩 대기 중...")
    for i in range(30):
        if find_target_window():
            print(f"✅ [감지] 프로그램 창이 감지되었습니다. ({i+1}초 소요)")
            time.sleep(5)
            return True
        time.sleep(1)
    
    print("❌ [실패] 프로그램이 실행되지 않았거나 창을 찾을 수 없습니다.")
    return False

def find_target_window():
    try:
        windows = Desktop(backend="uia").windows()
        for w in windows:
            if "e-Partner" in w.window_text() or "삼성생명" in w.window_text():
                return w
    except:
        pass
    return None

def login_process():
    print("🔑 [로그인] ID/PW 입력 시도...")
    w, h = pyautogui.size()
    pyautogui.click(w//2, h//2)
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(USER_ID)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    pyautogui.press('tab')
    pyperclip.copy(USER_PW)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    pyautogui.press('enter')
    print("✅ [입력] 로그인 정보 제출 완료.")

def handle_popups():
    print("🛡️ [팝업] 팝업 창 대기 (3초)...")
    time.sleep(3)
    pyautogui.click(POS_LOGIN_ALREADY_OK)
    print("✅ [클릭] 팝업 확인 버튼 클릭 (예상).")

def save_excel_generic(target_dir_name, file_prefix):
    """엑셀 저장 공통 로직 (F12)"""
    target_dir = os.path.join(r"g:\내 드라이브\안티그래비티\TEST", target_dir_name)
    os.makedirs(target_dir, exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(target_dir, f"{today_str}_{file_prefix}.xlsx")

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
    
    print("👋 [종료] 엑셀 닫기...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1.5)
    pyautogui.press('enter') # 저장 여부 팝업 엔터
    print(f"✅ 저장 완료: {os.path.basename(file_path)}")

def step1_contract_automation():
    print("\n======== [1단계] 계약관리 조회 시작 ========")
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
    
    # 엑셀 다운로드 프로세스
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
    
    # 엑셀 저장 창 및 인증 마법사 처리
    print("엑셀 로딩 및 인증 마법사 대기 (15초)...")
    time.sleep(15)
    print(f"인증 마법사 닫기 클릭: {POS_EXCEL_CLOSE_WIZARD}")
    pyautogui.click(POS_EXCEL_CLOSE_WIZARD)
    time.sleep(2)
    
    # 저장
    save_excel_generic("계약관리(일자별)", "계약일자별조회")

def step2_fee_automation():
    print("\n======== [2단계] 예상수수료 조회 시작 ========")
    
    # 메뉴 이동
    print("📂 [메뉴] '수수료_AFC' 이동 중...")
    pyautogui.click(POS_MENU_FEE_AFC)
    time.sleep(2)
    
    print("📂 [메뉴] '예상수수료조회_AFC' 클릭...")
    pyautogui.click(POS_SUBMENU_EXPECTED_FEE)
    time.sleep(5)
    
    # 생보L1 설정
    print("⚙️ [설정] '수수료레벨 생보L1' 설정...")
    pyautogui.click(POS_RADIO_LIFE_L1_STEP1)
    time.sleep(0.5)
    pyautogui.click(POS_RADIO_LIFE_L1_STEP2)
    time.sleep(1)

    # 손보L2 설정
    print("⚙️ [설정] '수수료레벨 손보L2' 설정...")
    pyautogui.click(POS_RADIO_NONLIFE_L2_STEP1)
    time.sleep(0.5)
    pyautogui.click(POS_RADIO_NONLIFE_L2_STEP2)
    time.sleep(1)
    
    # 조회
    print("🔍 [조회] 조회 버튼 클릭...")
    pyautogui.click(POS_Btn_INQUIRY_FEE)
    print("⏳ [대기] 조회 결과 대기 (7초)...")
    time.sleep(7)
    
    # 엑셀 다운로드
    print("💾 [엑셀] 다운로드 시작...")
    pyautogui.click(POS_Btn_EXCEL_FEE)
    time.sleep(3)
    
    # 사유 입력
    print("✍️ [입력] 다운로드 사유 입력...")
    pyautogui.click(POS_REASON_INPUT)
    time.sleep(1)
    pyautogui.write("upmuyong")
    time.sleep(1)
    pyautogui.click(POS_CONFIRM_BTN)
    
    print("⏳ [대기] 엑셀 뷰어 실행 대기 (15초)...")
    time.sleep(15)
    
    # 인증 마법사 닫기
    print("❌ [닫기] 엑셀 인증 마법사 닫기...")
    pyautogui.click(POS_EXCEL_CLOSE_WIZARD)
    time.sleep(2)
    
    # 저장
    save_excel_generic("수수료관리(일자별)", "예상수수료")
    
    # e-Partner 종료
    print("\n👋 [종료] 모든 다운로드 완료. e-Partner를 종료합니다.")
    os.system("taskkill /f /im XPlatform.exe /t >nul 2>&1")
    time.sleep(2)

def step3_update_master():
    print("\n======== [3단계] 마스터 파일(26년업적,수수료통계) 업데이트 ========")
    try:
        # 현재 스크립트의 위치를 기준으로 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        update_script = os.path.join(script_dir, "update_master_excel.py")
        
        # subprocess로 실행
        print(f"🔄 업데이트 스크립트 실행 중... (상세 내용은 아래 출력)")
        result = subprocess.run([sys.executable, update_script], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ [3단계 완료] 마스터 파일 업데이트 성공.")
        else:
            print("\n❌ [3단계 실패] 마스터 파일 업데이트 중 오류 발생.")
    except Exception as e:
        print(f"❌ [3단계 오류] {e}")

def main():
    max_retries = 3
    current_try = 0

    while current_try < max_retries:
        current_try += 1
        print(f"\n🚀 [통합 자동화] 전체 프로세스 시작 (시도 {current_try}/{max_retries})", flush=True)
        
        try:
            # 1. 초기화 (강제 종료)
            # clean_start는 XPlatform만 종료하므로, 엑셀도 확실히 종료
            print("🧹 [클린업] 기존 프로세스 정리 중...")
            clean_start() 
            os.system("taskkill /f /im EXCEL.EXE /t >nul 2>&1")
            time.sleep(2)

            # 2. 로그인 및 실행
            if not launch_application():
                raise Exception("e-Partner 실행 실패")
            login_process()
            handle_popups()
            
            print("\n메인 화면 진입 대기 (10초)...")
            time.sleep(10)
            
            # 3. 1단계 실행 (계약관리)
            step1_contract_automation()
            print("✅ [1단계 완료] 계약관리 수집 성공.")

            # e-Partner 창 활성화 확인 (엑셀 닫힌 후)
            print("\n🔄 [메뉴 전환] e-Partner 창 활성화 및 대기 (3초)...")
            time.sleep(3)
            w, h = pyautogui.size()
            pyautogui.click(w//2, h//2)
            time.sleep(1)

            # 4. 2단계 실행 (수수료)
            step2_fee_automation()
            print("✅ [2단계 완료] 예상수수료 수집 성공.")

            # 5. 3단계 실행 (마스터 업데이트)
            step3_update_master()

            print("\n🎉 [성공] 모든 데이터 수집 및 통합 자동화가 완료되었습니다!")
            break # 성공적으로 완료되면 루프 탈출

        except Exception as e:
            print(f"\n❌ [오류 발생] {e}")
            print(f"⚠️ 문제가 발생하여 프로그램을 초기화하고 처음부터 다시 시작합니다... (3초 대기)")
            time.sleep(3)
            # 다음 루프에서 clean_start()가 호출되어 프로세스 정리됨
            
    if current_try >= max_retries:
        print("\n❌ [최종 실패] 최대 재시도 횟수를 초과하여 자동화를 종료합니다.")

if __name__ == "__main__":
    main()
