import pandas as pd, sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx'
df_life = pd.read_excel(path, sheet_name='생명보험사_202602', nrows=2)
df_dmg  = pd.read_excel(path, sheet_name='손해보험사_202602', nrows=2)
print("=== 생명보험 전체 컬럼 ===")
for c in df_life.columns: print(" -", c)
print("\n=== 손해보험 전체 컬럼 ===")
for c in df_dmg.columns: print(" -", c)
print("\n=== 생명보험 샘플 데이터 ===")
print(df_life.to_string())
