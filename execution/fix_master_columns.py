"""
마스터 파일 컬럼 구조 강제 수정 + update_master_excel.py 핵심 로직 수정

[확정 컬럼 순서] A~BG (59개 고정)
  A(0)  : 체크사항
  B(1)  : FC코드
  C(2)  : FC명
  D(3)  : 제휴사
  E(4)  : 증권번호  ← KEY
  F(5)~BG(58) : 계약종류, 상품종류, ... , 37 (54개 고정)
  BG 이후 : 전부 삭제
"""
import pandas as pd
import shutil, datetime, sys, os

sys.stdout.reconfigure(encoding='utf-8')

FILE_MASTER = r"G:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"
SHEET_NAME  = "RAWDATA"

# ─────────────────────────────────────────────────────────────
# ★ 확정 고정 컬럼 순서 (A~BG, 59개)
#   이 순서가 진실이며, 스크립트는 항상 이 순서를 강제해야 함
# ─────────────────────────────────────────────────────────────
MASTER_COLUMNS = [
    # A~E: 기본 정보
    '체크사항',         # A
    'FC코드',           # B
    'FC명',             # C
    '제휴사',           # D
    '증권번호',         # E ← KEY (병합 기준)
    # F~: 계약 정보
    '계약종류',         # F
    '상품종류',         # G
    '상품명',           # H
    '보험료',           # I
    '보험사환산_1차년', # J
    '계약상태',         # K
    '계약일자',         # L
    '업적월',           # M
    '납입기간',         # N
    '익월시상',         # O
    '초회',             # P
    '익월시책',         # Q
    '2차년시책',        # R
    '1차년',            # S
    '2차년',            # T
    '3차년',            # U
    '계',               # V
    # W~BG: 월별 수수료 (1~37개월)
    '1','2','3','4','5','6','7','8','9','10',
    '11','12','13','14','15','16','17','18','19','20',
    '21','22','23','24','25','26','27','28','29','30',
    '31','32','33','34','35','36','37',
]
# 검증: 반드시 59개여야 함
assert len(MASTER_COLUMNS) == 59, f"컬럼 수 오류: {len(MASTER_COLUMNS)}개 (59개여야 함)"

print("=" * 60)
print("  마스터 파일 컬럼 구조 복구 시작")
print(f"  확정 컬럼: {len(MASTER_COLUMNS)}개 (A~BG)")
print("=" * 60)

# 백업
backup_dir = os.path.join(os.path.dirname(FILE_MASTER), "backup")
os.makedirs(backup_dir, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = os.path.join(backup_dir, f"backup_{ts}_컬럼복구전_{os.path.basename(FILE_MASTER)}")
shutil.copy2(FILE_MASTER, backup_path)
print(f"[백업] 완료: {os.path.basename(backup_path)}")

# 현재 마스터 로딩
all_sheets = pd.read_excel(FILE_MASTER, sheet_name=None)
df = all_sheets[SHEET_NAME].copy()

print(f"\n[현재] 컬럼 수: {len(df.columns)}개")
print(f"       행   수: {len(df):,}행")

# 현재 컬럼 목록 확인
print("\n[현재 컬럼 순서 문제 진단]")
for i, col in enumerate(MASTER_COLUMNS):
    cur_pos = list(df.columns).index(col) if col in df.columns else -1
    status = "OK" if cur_pos == i else f"❌ 현재위치={cur_pos}, 목표={i}"
    print(f"  {chr(65+i) if i < 26 else chr(64+i//26)+chr(65+i%26)}({i:02d}) {col:<20}: {status}")

# 없는 컬럼 확인 (MASTER_COLUMNS 기준으로 없으면 NaN으로 추가)
missing = [c for c in MASTER_COLUMNS if c not in df.columns]
if missing:
    print(f"\n[경고] 마스터에 없는 컬럼 {len(missing)}개 → NaN으로 추가: {missing}")
    for c in missing:
        df[c] = None

# 불필요한 컬럼 목록
extra = [c for c in df.columns if c not in MASTER_COLUMNS]
print(f"\n[삭제 대상] BG 이후 불필요 컬럼 {len(extra)}개:")
for c in extra:
    print(f"  - {c}")

# ★ 핵심: 컬럼 순서 강제 지정 + 불필요 컬럼 전부 제거
df_fixed = df[MASTER_COLUMNS].copy()

print(f"\n[수정 후] 컬럼 수: {len(df_fixed.columns)}개")
print(f"         행   수: {len(df_fixed):,}행")

# 확인 출력
print("\n[수정 후 컬럼 순서 확인]")
for i, col in enumerate(df_fixed.columns):
    excel_col = chr(65+i) if i < 26 else chr(64+(i//26))+chr(65+(i%26))
    print(f"  {excel_col}({i:02d}): {col}")

# 저장
all_sheets[SHEET_NAME] = df_fixed
with pd.ExcelWriter(FILE_MASTER, engine='openpyxl') as writer:
    for sn, ds in all_sheets.items():
        ds.to_excel(writer, sheet_name=sn, index=False)

print(f"\n{'=' * 60}")
print(f"[완료] 마스터 파일 컬럼 구조 복구 완료!")
print(f"  A(0) = 체크사항  |  E(4) = 증권번호  |  BG(58) = 37")
print(f"{'=' * 60}")
