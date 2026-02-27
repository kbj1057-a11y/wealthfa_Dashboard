"""
웰스FA - Flourish [Animated scatter Hans Rosling] 전용 CSV 변환기
----------------------------------------------------------------------
필요 포맷: LONG 포맷 (FC × 날짜별 1행)

컬럼 구성:
  FC명   | 그룹(색상) | 날짜(시간축) | 누적건수(X) | 누적실적(Y) | 누적실적(Size)

Flourish 매핑:
  X     → 누적건수  (가로 이동 - 얼마나 많이 움직였는가)
  Y     → 누적실적  (세로 이동 - 얼마나 많이 벌었는가)
  Size  → 누적실적  (버블 크기)
  Color → 그룹      (생명파트/손해파트)
  Time  → 날짜      (애니메이션 프레임)
  Label → FC명
"""
import pandas as pd
import os, sys, datetime

sys.stdout.reconfigure(encoding='utf-8')

# ── 경로
BASE     = os.path.dirname(os.path.abspath(__file__))
EXCEL    = os.path.join(BASE, "..", "매일업데이트", "26년종합.xlsx")
OUT_PATH = os.path.join(BASE, "..", "매일업데이트", "flourish_bubble_hans.csv")

# ── 분석 기간
START = datetime.date(2026, 2, 1)
END   = datetime.date.today()

LIFE_KEYWORDS = ["생명", "생보", "라이프"]

def is_life(company):
    if pd.isna(company): return False
    return any(kw in str(company) for kw in LIFE_KEYWORDS)

def main():
    print("=" * 55)
    print("  Flourish Animated Scatter (Hans Rosling) CSV 변환")
    print("=" * 55)

    # 1. 엑셀 로드
    xl    = pd.ExcelFile(EXCEL)
    sheet = "RAWDATA" if "RAWDATA" in xl.sheet_names else xl.sheet_names[0]
    raw   = pd.read_excel(EXCEL, sheet_name=sheet, engine='openpyxl')

    # 2. 컬럼 추출
    df = pd.DataFrame()
    df['FC명']    = raw.iloc[:, 2]
    df['제휴사']  = raw.iloc[:, 3]
    df['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
    p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    df['월P']  = p1 + p2
    df['날짜'] = df['계약일자'].dt.date
    df = df[df['FC명'].notna() & df['날짜'].notna()].copy()

    # 3. FC별 그룹 분류 (전체 기간 기준)
    df['is_life'] = df['제휴사'].apply(is_life)
    group_map = {}
    for fc, grp in df.groupby('FC명'):
        ratio = grp['is_life'].sum() / len(grp)
        group_map[fc] = "생명파트" if ratio >= 0.5 else "손해파트"

    # 4. 분석 기간 필터
    df = df[(df['날짜'] >= START) & (df['날짜'] <= END)]
    all_dates = pd.date_range(start=START, end=END, freq='D').date
    all_fcs   = sorted(df['FC명'].unique().tolist())

    print(f"FC 수: {len(all_fcs)}명 / 기간: {START} ~ {END} ({len(all_dates)}일)")

    # 5. FC별/일별 합계
    daily = (
        df.groupby(['FC명', '날짜'])
        .agg(일별실적=('월P', 'sum'), 일별건수=('월P', 'count'))
        .reset_index()
    )

    # 6. Long 포맷 생성 (FC × 날짜 전체 조합)
    idx   = pd.MultiIndex.from_product([all_fcs, all_dates], names=['FC명', '날짜'])
    base  = pd.DataFrame(index=idx).reset_index()
    base  = base.merge(daily, on=['FC명', '날짜'], how='left').fillna(0)

    # 7. 누적합 계산 (FC별로 따로)
    base = base.sort_values(['FC명', '날짜'])
    base['누적실적'] = base.groupby('FC명')['일별실적'].cumsum().round(0).astype(int)
    base['누적건수'] = base.groupby('FC명')['일별건수'].cumsum().astype(int)

    # 8. 그룹 및 날짜 포맷 추가
    base['그룹'] = base['FC명'].map(group_map).fillna('손해파트')
    base['날짜_표시'] = base['날짜'].apply(lambda d: f"{d.month}/{d.day}")

    # 9. Flourish용 컬럼 정리 (불필요 제거)
    result = base[['FC명', '그룹', '날짜_표시', '누적건수', '누적실적']].copy()
    result.columns = ['FC명', '그룹', '날짜', '누적건수(X)', '누적실적(Y/Size)']

    # 10. CSV 저장
    result.to_csv(OUT_PATH, index=False, encoding='utf-8-sig')

    # 보고
    life_n    = sum(1 for v in group_map.values() if v == "생명파트")
    nonlife_n = sum(1 for v in group_map.values() if v == "손해파트")
    rows      = len(result)

    print()
    print("=" * 55)
    print("  변환 완료!")
    print("=" * 55)
    print(f"  저장 경로: {OUT_PATH}")
    print(f"  총 행 수:  {rows:,}행 ({len(all_fcs)}명 × {len(all_dates)}일)")
    print(f"  생명파트:  {life_n}명  /  손해파트: {nonlife_n}명")
    print()
    print("[Flourish 'Animated scatter Hans...' 컬럼 매핑]")
    print("  X axis  → 누적건수(X)")
    print("  Y axis  → 누적실적(Y/Size)")
    print("  Size    → 누적실적(Y/Size)")
    print("  Color   → 그룹")
    print("  Time    → 날짜  ← 이게 애니메이션 슬라이더!")
    print("  Label   → FC명")

if __name__ == "__main__":
    main()
