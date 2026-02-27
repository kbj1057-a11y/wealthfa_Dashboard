import pandas as pd
import os
import sys
import datetime

# 터미널 출력 인코딩 설정 (윈도우 대응)
if sys.stdout.encoding != 'utf-8':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# ──── 설정값 ────────────────────────────────────────
DATA_PATH   = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년종합.xlsx"
OUTPUT_PATH = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\flourish_race_daily.csv"

# 분석 시작일 (2월 1일) ~ 종료일 (오늘)
START_DATE = datetime.date(2026, 2, 1)
END_DATE   = datetime.date.today()   # 자동으로 오늘 날짜 적용
# ────────────────────────────────────────────────────

def generate_daily_race():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return

    try:
        # 1. 엑셀 로드
        xl = pd.ExcelFile(DATA_PATH)
        sheet = "RAWDATA" if "RAWDATA" in xl.sheet_names else xl.sheet_names[0]
        raw = pd.read_excel(DATA_PATH, sheet_name=sheet, engine='openpyxl')

        # 2. 필요 컬럼 추출 (dashboard.py 동일 로직)
        df = pd.DataFrame()
        df['FC명']    = raw.iloc[:, 2]
        df['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
        p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)
        p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)
        df['월P']     = p1 + p2

        # 3. 유효 행만 남김
        df = df[df['FC명'].notna() & df['계약일자'].notna()].copy()
        df['날짜'] = df['계약일자'].dt.date

        # 4. 날짜 범위 필터 (2/1 ~ 오늘)
        df = df[(df['날짜'] >= START_DATE) & (df['날짜'] <= END_DATE)]
        
        if df.empty:
            print(f"Warning: No data found between {START_DATE} and {END_DATE}")
            return

        print(f"Data range: {df['날짜'].min()} ~ {df['날짜'].max()}  (Total {len(df)} records)")

        # 5. FC별/일별 합계
        pivot = (
            df.groupby(['FC명', '날짜'])['월P']
            .sum()
            .unstack(fill_value=0)
        )

        # 6. 시작일부터 오늘까지 모든 날짜 열 보장 (데이터 없는 날 = 0)
        all_dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D').date
        for d in all_dates:
            if d not in pivot.columns:
                pivot[d] = 0
        pivot = pivot.reindex(columns=sorted(pivot.columns))

        # 7. 누적합 (Bar Chart Race의 핵심: 매일마다 쌓이는 합산)
        race_df = pivot.cumsum(axis=1)

        # 8. 컬럼명을 Flourish가 읽기 좋게 변환 (예: 2/1, 2/2 ... 2/24)
        race_df.columns = [f"{d.month}/{d.day}" for d in race_df.columns]

        # 9. 소수점 제거 (정수로 저장 - 보기 좋게)
        race_df = race_df.round(0).astype(int)

        # 10. CSV 저장
        race_df.to_csv(OUTPUT_PATH, encoding='utf-8-sig')

        print(f"SUCCESS: {OUTPUT_PATH}")
        print(f"Total FCs: {len(race_df)}")
        print(f"Date columns: {list(race_df.columns)}")

    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    generate_daily_race()
