import pandas as pd
path = r'G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx'
df_life = pd.read_excel(path, sheet_name='생명보험사_202602')
df_life['계약일자_정제'] = pd.to_datetime(df_life['계약일자'], errors='coerce').dt.strftime('%Y-%m-%d')
df_life = df_life.rename(columns={'환산성적':'업적지표1','보험료':'업적지표2'})
is_jan = df_life['계약일자_정제'].str.startswith('2026-01', na=False)
print('1월 계약 생명보험 건수:', is_jan.sum())
print('환산성적(업적지표1) 합계:', df_life[is_jan]['업적지표1'].sum())
print('보험료(업적지표2) 합계:', df_life[is_jan]['업적지표2'].sum())
print('샘플 날짜:', df_life['계약일자_정제'].dropna().head(5).tolist())
