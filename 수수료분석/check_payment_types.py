import pandas as pd
df1 = pd.read_excel(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx', sheet_name='생명보험사_202602')
df2 = pd.read_excel(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx', sheet_name='손해보험사_202602')

print("=== 생명 지급구분 ===")
if '지급구분' in df1.columns:
    print(df1['지급구분'].value_counts(dropna=False))

print("\n=== 손해 지급구분 ===")
if '지급구분' in df2.columns:
    print(df2['지급구분'].value_counts(dropna=False))
