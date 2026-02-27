import subprocess, os, shutil, sys, datetime

# ── 설정값 ──────────────────────────────────────────────────
TOKEN   = "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"
REMOTE  = f"https://{TOKEN}@github.com/kbj1057-a11y/wealthfa_Dashboard.git"

# 이 스크립트 위치(TEST 폴더)를 기준으로 경로 자동 계산
BASE    = os.path.dirname(os.path.abspath(__file__))
SRC     = BASE  # g:\내 드라이브\안티그래비티\TEST
# ────────────────────────────────────────────────────────────

def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if result.stdout.strip():
        print(result.stdout.strip())
    return result.returncode

def main():
    print("[1/5] 임시 배포 환경 생성 중...")
    tmp = os.path.join(os.environ["TEMP"], f"wfa_{datetime.datetime.now().strftime('%H%M%S')}")
    tmp_data = os.path.join(tmp, "매일업데이트")
    os.makedirs(tmp_data, exist_ok=True)

    print("[2/5] 파일 복사 중...")
    files = {
        os.path.join(SRC, "dashboard.py"):                    os.path.join(tmp, "dashboard.py"),
        os.path.join(SRC, "requirements.txt"):                os.path.join(tmp, "requirements.txt"),
        os.path.join(SRC, "매일업데이트", "26년종합.xlsx"):   os.path.join(tmp_data, "26년종합.xlsx"),
    }
    for src_path, dst_path in files.items():
        if not os.path.exists(src_path):
            print(f"  오류: 파일 없음 → {src_path}")
            shutil.rmtree(tmp, ignore_errors=True)
            sys.exit(1)
        shutil.copy2(src_path, dst_path)
        print(f"  OK: {os.path.basename(dst_path)}")

    print("[3/5] Git 초기화 중...")
    run(["git", "init"],                         cwd=tmp)
    run(["git", "config", "user.email", "deploy@wealthfa.com"], cwd=tmp)
    run(["git", "config", "user.name",  "WealthFA-Bot"],        cwd=tmp)
    run(["git", "remote", "add", "origin", REMOTE],             cwd=tmp)

    print("[4/5] 커밋 중...")
    run(["git", "add", "-A"], cwd=tmp)
    msg = f"data-update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    code = run(["git", "commit", "-m", msg], cwd=tmp)
    if code != 0:
        print("  커밋 실패 (변경 내용 없음?)")
        shutil.rmtree(tmp, ignore_errors=True)
        sys.exit(1)

    print("[5/5] GitHub 전송 중...")
    run(["git", "branch", "-M", "main"], cwd=tmp)
    code = run(["git", "push", "origin", "main", "--force"], cwd=tmp)

    shutil.rmtree(tmp, ignore_errors=True)

    if code == 0:
        print()
        print("==========================================")
        print("  배포 성공!")
        print("  https://wealhfa.streamlit.app/")
        print("==========================================")
    else:
        print("  전송 실패! 토큰 또는 인터넷 확인 필요.")
        sys.exit(1)

if __name__ == "__main__":
    main()
