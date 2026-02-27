import pyautogui
import time

def get_mouse_pos():
    print("3초 뒤 마우스 좌표를 기록합니다...")
    print("원하는 위치(예상수수료 메뉴)에 마우스를 올리세요!")
    
    for i in range(3, 0, -1):
        print(f"{i}초 전...", end='\r')
        time.sleep(1)
        
    x, y = pyautogui.position()
    print(f"\n✅ 기록된 좌표: ({x}, {y})")
    
if __name__ == "__main__":
    get_mouse_pos()
