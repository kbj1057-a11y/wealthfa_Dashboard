from pywinauto import Application, Desktop
import time

def analyze_epartner_window():
    try:
        print("e-Partner 창을 분석합니다...")
        # 'e-Partner'라는 제목의 창을 찾습니다.
        app = Application(backend="uia").connect(title="e-Partner", timeout=10)
        main_win = app.window(title="e-Partner")
        
        print(f"창 핸들: {main_win.handle}")
        main_win.set_focus()
        
        print("\n[자식 컨트롤 목록]")
        # 모든 하위 컨트롤(버튼, 입력창 등)을 출력합니다.
        # 화면 보안이 작동하더라도 UIA를 통한 구조 분석은 가능할 수 있습니다.
        main_win.print_control_identifiers()
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print("e-Partner 창을 찾을 수 없거나 접근이 거부되었습니다.")

if __name__ == "__main__":
    analyze_epartner_window()
