
import pyautogui
import time
import sys
import json

# 한글 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

STEPS = [
    "1. [메뉴] 수수료_AFC (클릭)",
    "2. [서브메뉴] 예상수수료조회_AFC (클릭)",
    "3. [옵션] 생보L1 - 첫번째 클릭 (라디오버튼 등)",
    "4. [옵션] 생보L1 - 두번째 클릭 (확인 등)",
    "5. [옵션] 손보L2 - 첫번째 클릭 (라디오버튼 등)",
    "6. [옵션] 손보L2 - 두번째 클릭 (확인 등)",
    "7. [버튼] 조회",
    "8. [버튼] 엑셀다운로드"
]

def record_coordinates():
    results = {}
    print("=" * 50)
    print("🖱️ 마우스 좌표 기록 도우미 (재시작)")
    print("각 단계별로 마우스를 해당 위치에 올린 후 'Enter' 키를 누르세요.")
    print("=" * 50)

    for step in STEPS:
        # 안내 메시지 출력
        print(f"\n👉 {step} 위치에 마우스를 올리고 [Enter]를 누르세요...", end='', flush=True)
        sys.stdout.flush()
        
        # 입력 대기
        input()
        
        # 좌표 획득
        x, y = pyautogui.position()
        print(f"   ✅ 좌표 저장됨: ({x}, {y})")
        results[step] = (x, y)
        time.sleep(0.5)

    print("\n" + "=" * 50)
    print("🎉 모든 좌표 기록 완료!")
    print("=" * 50)
    
    # 결과 출력
    for k, v in results.items():
        print(f"{k}: {v}")

    # 파일로 저장
    with open("fee_coordinates.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("\n📁 'fee_coordinates.json' 파일로 저장되었습니다.")

if __name__ == "__main__":
    record_coordinates()
