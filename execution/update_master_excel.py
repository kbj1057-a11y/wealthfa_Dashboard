"""
═══════════════════════════════════════════════════════════════
  마스터 파일 업데이트 스크립트 (전면 재작성)
  파일: update_master_excel.py

  [확정 처리 흐름]
  ┌─ Step 1. 수수료파일 → 마스터
  │   · 증권번호 기준
  │   · 마스터에 없는 증권번호만 → 전체 컬럼 추가
  │   · 마스터에 있는 증권번호   → 건드리지 않음 (스킵)
  │
  ├─ Step 2. 계약파일 → 마스터
  │   · 증권번호 기준 (계약파일 컬럼명: 'y')
  │   · 마스터에 있는 증권번호   → 납입기간 숫자만 업데이트
  │   · 마스터에 없는 증권번호   → 스킵
  │
  └─ Step 3. 컬럼 구조 강제 정렬 (A~BG, 59개 고정) → 저장

  [마스터 컬럼 구조 고정]
  A 체크사항 | B FC코드 | C FC명 | D 제휴사 | E 증권번호
  F 계약종류 ~ BG 37 (54개 고정)
  → BG 이후 컬럼은 절대 유입 불가
═══════════════════════════════════════════════════════════════
"""

import pandas as pd
import glob
import os
import re
import shutil
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════
# ★ 경로 설정
# ═══════════════════════════════════════
DIR_FEE      = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
FILE_MASTER  = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"
SHEET_NAME   = "RAWDATA"

# ═══════════════════════════════════════
# ★ 컬럼 설정
# ═══════════════════════════════════════

# 마스터 고정 컬럼 (A~BG, 59개) - 이 순서가 진실
MASTER_COLUMNS = [
    # A~E: 기본 정보
    '체크사항',          # A(0)  - 수동 입력
    'FC코드',            # B(1)
    'FC명',              # C(2)
    '제휴사',            # D(3)
    '증권번호',          # E(4)  ← 병합 KEY
    # F~L: 계약 기본
    '계약종류',          # F(5)
    '상품종류',          # G(6)
    '상품명',            # H(7)
    '보험료',            # I(8)
    '보험사환산_1차년',  # J(9)
    '계약상태',          # K(10)
    '계약일자',          # L(11)
    # M~V: 업적 및 수수료 요약
    '업적월',            # M(12) - 수동/계산
    '납입기간',          # N(13) ← 계약파일에서 업데이트 (숫자만)
    '익월시상',          # O(14) - 수동 입력
    '초회',              # P(15) - 수수료파일
    '익월시책',          # Q(16) - 수동 입력
    '2차년시책',         # R(17) - 수동 입력
    '1차년',             # S(18)
    '2차년',             # T(19)
    '3차년',             # U(20)
    '계',                # V(21)
    # W~BG: 월별 수수료 1~37회차
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    '31', '32', '33', '34', '35', '36', '37',
]
assert len(MASTER_COLUMNS) == 59, f"컬럼 수 오류: {len(MASTER_COLUMNS)}개"

# 수수료파일 → 마스터 컬럼 매핑 (수수료파일 컬럼명: 마스터 컬럼명)
# 이름이 같으면 자동 매핑, 다른 경우만 명시
FEE_COL_MAP = {
    # 수수료파일의 컬럼명이 마스터와 동일한 경우는 별도 표기 불필요
    # (아래는 혹시 이름이 다를 경우를 위한 예비 매핑)
    # 'fee_col_name': 'master_col_name',
}

# 계약파일에서 증권번호 역할 컬럼명 ('y'로 다운로드됨)
CONTRACT_ID_COL = 'y'

# ═══════════════════════════════════════
# 유틸 함수
# ═══════════════════════════════════════

def get_latest_file(directory, pattern="*.xlsx"):
    """폴더에서 가장 최신 엑셀 파일 반환"""
    files = glob.glob(os.path.join(directory, pattern))
    files = [f for f in files if not os.path.basename(f).startswith("~$")]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def backup_master():
    """마스터 파일 타임스탬프 백업"""
    if not os.path.exists(FILE_MASTER):
        return
    backup_dir = os.path.join(os.path.dirname(FILE_MASTER), "backup")
    os.makedirs(backup_dir, exist_ok=True)
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_dir, f"backup_{ts}_{os.path.basename(FILE_MASTER)}")
    shutil.copy2(FILE_MASTER, dest)
    print(f"  [백업] {os.path.basename(dest)}")


def extract_number(value) -> int | None:
    """
    납입기간 숫자 추출
      20        → 20
      20.0      → 20
      "20년납"  → 20
      None/nan  → None
    """
    if value is None:
        return None
    s = str(value).strip()
    if s in ('', 'nan', 'None', 'NaN'):
        return None
    # 숫자만 추출
    digits = re.sub(r'[^\d]', '', s.split('.')[0])
    return int(digits) if digits else None


def enforce_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    마스터 컬럼 순서를 MASTER_COLUMNS 기준으로 강제 정렬
    없는 컬럼은 None / 불필요 컬럼은 제거
    """
    for col in MASTER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    removed = [c for c in df.columns if c not in MASTER_COLUMNS]
    if removed:
        print(f"  [정리] 불필요 컬럼 {len(removed)}개 제거: {removed}")
    return df[MASTER_COLUMNS].copy()


# ═══════════════════════════════════════
# ■ 핵심 로직
# ═══════════════════════════════════════

def step1_add_new_from_fee(df_master: pd.DataFrame,
                            df_fee: pd.DataFrame) -> pd.DataFrame:
    """
    [Step 1] 수수료파일 → 마스터 신규 추가
    - 증권번호가 마스터에 없는 행만 추가
    - 기존 행은 절대 건드리지 않음
    """
    print("\n[Step 1] 수수료파일 → 마스터 신규 추가")

    # 증권번호 문자열 통일
    master_ids = set(df_master['증권번호'].astype(str).str.strip())
    df_fee     = df_fee.copy()
    df_fee['증권번호'] = df_fee['증권번호'].astype(str).str.strip()

    # 마스터에 없는 행만 필터
    new_rows = df_fee[~df_fee['증권번호'].isin(master_ids)].copy()

    if new_rows.empty:
        print("  → 신규 추가 건 없음")
        return df_master

    print(f"  → 신규 {len(new_rows)}건 발견:")
    for _, row in new_rows.iterrows():
        print(f"     증권번호={row.get('증권번호','?')} | "
              f"제휴사={row.get('제휴사','?')} | "
              f"FC명={row.get('FC명','?')} | "
              f"계약일={row.get('계약일자','?')}")

    # MASTER_COLUMNS 기준으로 컬럼 맞춤 후 concat
    available = [c for c in MASTER_COLUMNS if c in new_rows.columns]
    new_rows_mapped = new_rows[available].copy()

    df_result = pd.concat([df_master, new_rows_mapped], axis=0, ignore_index=True)
    print(f"  ✅ {len(new_rows)}건 추가 완료 "
          f"(이전 {len(df_master)}건 → 이후 {len(df_result)}건)")
    return df_result


def step2_update_납입기간(df_master: pd.DataFrame,
                         df_contract: pd.DataFrame) -> pd.DataFrame:
    """
    [Step 2] 계약파일 → 납입기간(숫자만) 업데이트
    - 계약파일 'y' 컬럼 = 증권번호
    - 마스터에 있는 증권번호만 업데이트
    - 숫자만 추출 (20.0 → 20, "20년납" → 20)
    """
    print("\n[Step 2] 계약파일 → 납입기간 업데이트")

    df_contract = df_contract.copy()

    # 'y' 컬럼 → 증권번호 rename
    if CONTRACT_ID_COL in df_contract.columns:
        df_contract = df_contract.rename(columns={CONTRACT_ID_COL: '증권번호'})
    elif '증권번호' not in df_contract.columns:
        print("  ✗ 계약파일에서 증권번호 컬럼을 찾을 수 없습니다. Step 2 스킵.")
        return df_master

    df_contract['증권번호'] = df_contract['증권번호'].astype(str).str.strip()

    # 납입기간 컬럼 확인
    if '납입기간' not in df_contract.columns:
        print("  ✗ 계약파일에 납입기간 컬럼이 없습니다. Step 2 스킵.")
        return df_master

    # 증권번호별 납입기간 매핑 (중복 시 첫 번째)
    pay_map = (df_contract[['증권번호', '납입기간']]
               .drop_duplicates(subset='증권번호')
               .set_index('증권번호')['납입기간'])

    df_master = df_master.copy()
    df_master['증권번호'] = df_master['증권번호'].astype(str).str.strip()

    updated_count = 0
    skipped_none  = 0

    for i, row in df_master.iterrows():
        pid = row['증권번호']
        if pid not in pay_map.index:
            continue  # 계약파일에 없으면 스킵

        raw_val = pay_map[pid]
        num = extract_number(raw_val)

        if num is None:
            skipped_none += 1
            continue

        df_master.at[i, '납입기간'] = num
        updated_count += 1

    print(f"  ✅ 납입기간 업데이트: {updated_count}건 | 값 없어 스킵: {skipped_none}건")
    return df_master


# ═══════════════════════════════════════
# ■ 메인 실행
# ═══════════════════════════════════════

def update_master():
    print("=" * 60)
    print("  마스터 파일 업데이트 시작")
    print(f"  실행 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 파일 탐색
    latest_fee      = get_latest_file(DIR_FEE)
    latest_contract = get_latest_file(DIR_CONTRACT)

    if not latest_fee:
        print("✗ 수수료 파일이 없습니다.")
        return
    if not latest_contract:
        print("✗ 계약 파일이 없습니다.")
        return

    print(f"\n  수수료파일 : {os.path.basename(latest_fee)}")
    print(f"  계약파일   : {os.path.basename(latest_contract)}")
    print(f"  마스터파일 : {os.path.basename(FILE_MASTER)}")

    try:
        # ── 백업
        backup_master()

        # ── 파일 로딩
        df_master   = pd.read_excel(FILE_MASTER, sheet_name=SHEET_NAME, dtype=str)
        df_fee      = pd.read_excel(latest_fee,      dtype=str)
        df_contract = pd.read_excel(latest_contract,  dtype=str)

        # 마스터 초기 현황
        master_before = len(df_master)
        print(f"\n  마스터 시작: {master_before:,}건")

        # ── Step 1: 수수료파일 신규 추가
        df_master = step1_add_new_from_fee(df_master, df_fee)

        # ── Step 2: 계약파일 납입기간 업데이트
        df_master = step2_update_납입기간(df_master, df_contract)

        # ── Step 3: 컬럼 구조 강제 정렬 + 저장
        print("\n[Step 3] 컬럼 구조 강제 정렬 (A=체크사항, E=증권번호, BG=37)")
        df_master = enforce_columns(df_master)
        print(f"  최종 컬럼: {len(df_master.columns)}개 (A~BG 고정)")

        print("\n  저장 중...")
        all_sheets = pd.read_excel(FILE_MASTER, sheet_name=None)
        all_sheets[SHEET_NAME] = df_master

        with pd.ExcelWriter(FILE_MASTER, engine='openpyxl') as writer:
            for sn, ds in all_sheets.items():
                ds.to_excel(writer, sheet_name=sn, index=False)

        # ── 최종 결과
        print(f"\n{'=' * 60}")
        print(f"  ✅ 업데이트 완료!")
        print(f"  업데이트 전: {master_before:,}건")
        print(f"  업데이트 후: {len(df_master):,}건")
        print(f"  신규 추가  : {len(df_master) - master_before:,}건")
        print(f"  컬럼 구조  : A=체크사항 | E=증권번호 | BG=37 (59개 고정)")
        print(f"{'=' * 60}")

    except Exception as e:
        import traceback
        print(f"\n✗ 오류 발생: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    update_master()
