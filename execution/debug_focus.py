import time
from pywinauto import Application, Desktop
import pyautogui

def debug_window():
    try:
        print("e-Partner 창 정보를 상세 분석합니다...")
        # 모든 'e-Partner' 타이틀 창을 찾습니다.
        windows = Desktop(backend="uia").windows(title="e-Partner")
        
        if not windows:
            print("e-Partner 창을 찾을 수 없습니다.")
            return

        for i, w in enumerate(windows):
            rect = w.rectangle()
            print(f"[{i}] 창 발견: {w.window_text()}")
            print(f"    좌표: Left={rect.left}, Top={rect.top}, Right={rect.right}, Bottom={rect.bottom}")
            print(f"    크기: {rect.width()}x{rect.height()}")
            
            # 너무 작은 창(트레이 아이콘 등)은 제외하고 실제 화면에 보이는 창 선택
            if rect.width() > 100 and rect.height() > 100:
                print("    ==> 유효한 로그인 창으로 추정됩니다. 강제 활성화 시도...")
                w.set_focus()
                
                # 창의 정중앙 클릭 (포커스 확실히 잡기)
                center_x = rect.left + (rect.width() // 2)
                center_y = rect.top + (rect.height() // 2)
                print(f"    중앙 좌표 클릭: ({center_x}, {center_y})")
                pyautogui.click(center_x, center_y)
                time.sleep(1)
                
                # 테스트로 텍스트 입력 시도
                pyautogui.write("test_id")
                print("    테스트 텍스트 'test_id' 입력 완료. 화면에 변화가 있는지 확인해 주세요.")
                break

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    debug_window()
