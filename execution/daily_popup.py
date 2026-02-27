
import sys
import random
import subprocess

# 한글 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# 🎲 랜덤 메시지 리스트
MESSAGES = [
    "☕ 따뜻한 커피 한 잔 어때요?\n\n안티그래비티가 1분 뒤 업무를 시작합니다!",
    "🙆‍♂️ 잠시 자리에서 일어나 스트레칭 하세요!\n\n자동화 작업은 제가 맡겠습니다. (60초 대기)",
    "🤖 주인님은 편히 쉬세요, 일은 제가 합니다.\n\n1분 뒤에 자동으로 시작할게요!",
    "✨ 오늘도 긍정적인 하루 보내세요!\n\n데이터 수집 준비 완료. (60초 뒤 시작)",
    "🎵 좋아하는 음악 한 곡 들으면서 여유를 즐기세요.\n\n잠시 후 자동화가 시작됩니다.",
    "🚀 준비 완료! 엔진 예열 중...\n\n60초 뒤에 자동으로 출발합니다!",
    "💤 잠깐 눈을 감고 휴식을 취해보세요.\n\n나머지는 안티그래비티에게 맡겨주세요.",
    "🍀 오늘 행운이 가득하길 바랍니다!\n\n1분 카운트다운 시작합니다."
]

def show_popup():
    """랜덤 메시지로 60초 타임아웃 팝업 띄우기"""
    msg = random.choice(MESSAGES)
    
    # PowerShell 스크립트 생성 (WScript.Shell Popup 사용)
    # Popup(Message, SecondsToWait, Title, Type)
    # Type 1 (OK/Cancel) + 64 (Information Icon) = 65
    # Return: 1=OK, 2=Cancel, -1=Timeout
    ps_command = f"""
    $wsh = New-Object -ComObject Wscript.Shell
    $result = $wsh.Popup('{msg}', 60, '안티그래비티의 아침 인사', 1 + 64)
    
    # 취소(2)를 누르면 종료 코드 1 반환, 나머지는 0 (진행)
    if ($result -eq 2) {{ exit 1 }} else {{ exit 0 }}
    """
    
    # PowerShell 실행
    try:
        # subprocess.run을 사용하되, 창을 숨기거나 최소화할 필요는 없음 (팝업만 뜨면 됨)
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=False)
        return result.returncode
    except Exception as e:
        print(f"팝업 실행 실패: {e}")
        return 0 # 실패 시 그냥 진행

if __name__ == "__main__":
    # 팝업 결과에 따라 종료 코드 반환 (0: 진행, 1: 취소)
    sys.exit(show_popup())
