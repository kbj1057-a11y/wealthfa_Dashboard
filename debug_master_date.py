import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"
SHEET_NAME = "RAWDATA"

df_master = pd.read_excel(FILE_MASTER, sheet_name=SHEET_NAME)

# 마스터 파일의 '계약일자' 컬럼 찾기
print("=== 마스터 파일 컬럼 중 날짜/계약 관련 확인 ===")
for col in df_master.columns:
    if '계약' in str(col) or '일자' in str(col) or '날짜' in str(col) or '날' in str(col):
        print(f"컬럼: {col}")
        print(df_master[col].dropna().head(5))
        print()

print("=== 마스터 파일 전체 컬럼명 ===")
for i, col in enumerate(df_master.columns):
    print(f"{i}: {col}")

print(f"\n마스터 파일 총 행 수: {len(df_master)}")
