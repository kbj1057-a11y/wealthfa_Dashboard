import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년종합.xlsx"
EXCLUDE_FC = ['임정일']

raw = pd.read_excel(FILE, sheet_name="RAWDATA")

raw['FC명'] = raw.iloc[:, 2]
raw['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)
p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)
raw['월P'] = p1 + p2

df_feb = raw[(raw['계약일자'].dt.year == 2026) & (raw['계약일자'].dt.month == 2)]
df_feb = df_feb[~df_feb['FC명'].isin(EXCLUDE_FC)]

# 월P MVP
top_p = df_feb.groupby('FC명')['월P'].sum().sort_values(ascending=False)
mvp_p_name = top_p.index[0]

# 활동(건수) MVP
top_cnt = df_feb.groupby('FC명').size().sort_values(ascending=False)
mvp_cnt_name = top_cnt.index[0]
mvp_cnt_val = int(top_cnt.iloc[0])

print(f"월P MVP: {mvp_p_name}")
print(f"활동 MVP: {mvp_cnt_name} ({mvp_cnt_val}건)")
