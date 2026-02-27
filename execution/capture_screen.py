import pyautogui
import time
import os
from pathlib import Path

def capture_screen():
    # .tmp 디렉토리 생성
    tmp_dir = Path("g:/내 드라이브/안티그래비티/TEST/.tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = tmp_dir / f"screen_{timestamp}.png"
    
    print(f"화면 캡처 중: {screenshot_path}")
    screenshot = pyautogui.screenshot()
    screenshot.save(str(screenshot_path))
    print("캡처 완료.")
    return screenshot_path

if __name__ == "__main__":
    # 실행 전 3초 대기 (사용자가 화면을 준비할 시간)
    print("3초 후 화면을 캡처합니다. 원하는 화면을 띄워주세요.")
    time.sleep(3)
    capture_screen()
