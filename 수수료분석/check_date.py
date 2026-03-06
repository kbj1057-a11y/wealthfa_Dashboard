import pandas as pd
df_life = pd.read_excel(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx', sheet_name='생명보험사_202602')
df_dmg = pd.read_excel(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx', sheet_name='손해보험사_202602')

print("=== 생명보험사 계약일자 샘플 ===")
if '계약일자' in df_life.columns:
    print(df_life['계약일자'].head(10).tolist())
    
print("\n=== 손해보험사 계약일자 샘플 ===")
if '계약일자' in df_dmg.columns:
    print(df_dmg['계약일자'].head(10).tolist())
