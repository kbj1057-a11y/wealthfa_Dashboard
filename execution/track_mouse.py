import pyautogui
import time
import sys

# 한글 출력 깨짐 방지
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

def track_mouse():
    print("마우스 좌표 추적을 시작합니다. (Ctrl+C로 종료)")
    print("원하는 위치에 마우스를 올리고 좌표를 기록하세요.")
    
    try:
        while True:
            x, y = pyautogui.position()
            # print(f"현재 좌표: ({x}, {y})", end='\r') # 한 줄 업데이트 (터미널에 따라 안 보일 수 있음)
            print(f"현재 좌표: ({x}, {y})") # 그냥 줄바꿈해서 출력
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n좌표 추적 종료.")

if __name__ == "__main__":
    track_mouse()
