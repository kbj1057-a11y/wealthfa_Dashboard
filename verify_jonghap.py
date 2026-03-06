import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년종합.xlsx"

xl = pd.ExcelFile(FILE)
print(f"시트 목록: {xl.sheet_names}")

sheet = "RAWDATA" if "RAWDATA" in xl.sheet_names else xl.sheet_names[0]
raw = pd.read_excel(FILE, sheet_name=sheet)

print(f"\n사용 시트: {sheet}")
print(f"총 행 수: {len(raw)}")
print(f"총 컬럼 수: {len(raw.columns)}")
print("\n=== 컬럼 인덱스 매핑 확인 ===")
for i, col in enumerate(raw.columns):
    sample = raw.iloc[0, i] if len(raw) > 0 else "N/A"
    print(f"Index {i:2d}: [{col}] | 샘플: {sample}")

# 핵심 컬럼 확인
print("\n=== 핵심 데이터 샘플 (상위 5행) ===")
key_cols = [2, 3, 8, 9, 11, 15, 16]
for idx in key_cols:
    if idx < len(raw.columns):
        col_name = raw.columns[idx]
        samples = raw.iloc[:5, idx].tolist()
        print(f"Index {idx} [{col_name}]: {samples}")

# 월P 합계 확인
p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)
p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)
monthly_p = p1 + p2
print(f"\n월P (15+16번) 합계: {int(monthly_p.sum()):,}")
print(f"월P > 0 건수: {(monthly_p > 0).sum()}")

# FC명별 월P 합산 상위 10
raw['FC명'] = raw.iloc[:, 2]
raw['월P'] = monthly_p
raw['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
df_feb = raw[(raw['계약일자'].dt.year == 2026) & (raw['계약일자'].dt.month == 2)]
print(f"\n2월 데이터 행 수: {len(df_feb)}")
print("\nFC별 월P 합산 TOP10:")
print(df_feb.groupby('FC명')['월P'].sum().sort_values(ascending=False).head(10))
