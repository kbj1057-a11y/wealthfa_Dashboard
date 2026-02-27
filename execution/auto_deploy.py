import subprocess
import os
import datetime

# ─────────────────────────────────────────────
# 설정 (사용자 정보)
# ─────────────────────────────────────────────
GITHUB_TOKEN = "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"
GITHUB_REPO  = "github.com/kbj1057-a11y/wealthfa_Dashboard.git"
BRANCH       = "main"

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e.stderr}")
        return False
    return True

def main():
    print(f"🚀 배포를 시작합니다... ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    # 작업 디렉토리를 프로젝트 루트로 이동 (대개 한 단계 위)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..") 

    # 1. 변경사항 추가
    print("[1/3] 변경된 파일 수집 중...")
    run_git_command("git add .")

    # 2. 커밋 (메모 남기기)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[2/3] 업데이트 기록 작성 중: {now_str}")
    run_git_command(f'git commit -m "Auto-update data: {now_str}"')

    # 3. 푸시 (전송)
    # 토큰을 주소에 포함시켜 인증 절차 없이 통과
    remote_url = f"https://{GITHUB_TOKEN}@{GITHUB_REPO}"
    print("[3/3] 깃허브 서버로 데이터 전송 중...")
    if run_git_command(f"git push {remote_url} {BRANCH}"):
        print("\n✅ 배포가 완료되었습니다! 5~10초 내에 웹사이트에 반영됩니다.")
    else:
        print("\n❌ 배포에 실패했습니다. 네트워크 상태나 토큰을 확인해 주세요.")

if __name__ == "__main__":
    main()
