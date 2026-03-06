"""
v3 통합 파일을 deploy/data/ 폴더에 복사
"""
import os, shutil, sys

SRC  = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
DEST_DIR  = r"G:\내 드라이브\안티그래비티\TEST\deploy\data"
DEST_FILE = os.path.join(DEST_DIR, "최종병합_수수료명세서_압축판.xlsx")

os.makedirs(DEST_DIR, exist_ok=True)
shutil.copy2(SRC, DEST_FILE)

print(f"[완료] 복사 성공!", file=sys.stderr)
print(f"  원본: {SRC}", file=sys.stderr)
print(f"  대상: {DEST_FILE}", file=sys.stderr)
print(f"  크기: {os.path.getsize(DEST_FILE):,} bytes", file=sys.stderr)
