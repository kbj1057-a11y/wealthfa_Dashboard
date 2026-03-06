path = r'G:\내 드라이브\안티그래비티\TEST\temp_push\app.py'
with open(path, 'r', encoding='utf-8') as f:
    t = f.read()

# 기존 날짜 정제 코드를 정수형(YYYYMMDD) 처리 방식으로 교체
old = (
    "    # 날짜 정제\n"
    "    if '계약일자' in df_all.columns:\n"
    "        df_all['계약일자_정제'] = pd.to_datetime(df_all['계약일자'], errors='coerce').dt.strftime('%Y-%m-%d')\n"
    "    else:\n"
    "        df_all['계약일자_정제'] = ''\n"
)
new = (
    "    # 날짜 정제 (계약일자가 20260107 같은 정수형(int)으로 저장됨)\n"
    "    if '계약일자' in df_all.columns:\n"
    "        df_all['계약일자_정제'] = pd.to_datetime(\n"
    "            df_all['계약일자'].astype(str).str.zfill(8),\n"
    "            format='%Y%m%d', errors='coerce'\n"
    "        ).dt.strftime('%Y-%m-%d').fillna('')\n"
    "    else:\n"
    "        df_all['계약일자_정제'] = ''\n"
)

t = t.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(t)

# 검증
count = t.count("format='%Y%m%d'")
print(f"수정 완료: format='%Y%m%d' {count}개 적용됨")

# 로컬에서 실제 동작 확인
import pandas as pd
excel_path = r'G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx'
df_life = pd.read_excel(excel_path, sheet_name='생명보험사_202602')
df_life['계약일자_정제'] = pd.to_datetime(
    df_life['계약일자'].astype(str).str.zfill(8),
    format='%Y%m%d', errors='coerce'
).dt.strftime('%Y-%m-%d').fillna('')
is_jan = df_life['계약일자_정제'].str.startswith('2026-01', na=False)
df_life = df_life.rename(columns={'환산성적':'업적지표1','보험료':'업적지표2'})
print('1월 계약 건수:', is_jan.sum())
print('환산성적 합계:', df_life[is_jan]['업적지표1'].sum())
print('보험료 합계:', df_life[is_jan]['업적지표2'].sum())
