import pandas as pd
path = r'G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx'
df_life = pd.read_excel(path, sheet_name='생명보험사_202602')
print('계약일자 컬럼 dtype:', df_life['계약일자'].dtype)
print('계약일자 샘플 raw값:', df_life['계약일자'].head(5).tolist())
