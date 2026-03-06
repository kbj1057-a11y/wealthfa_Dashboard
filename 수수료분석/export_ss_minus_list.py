import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"
OUTPUT_FILE = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\삼성생명_마이너스환수_오류목록.xlsx"

print("="*60)
print("삼성생명 마이너스 환수(유형1) 모든 증권번호 추출 중...")
print("="*60)

# 데이터 준비
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')
df1_ss = df1[df1['제휴사명'].astype(str).str.contains('삼성생명', na=False)].copy()
df1_ss['수수료계'] = pd.to_numeric(df1_ss['수수료계'], errors='coerce').fillna(0)
df1_ss['증권번호'] = df1_ss['증권번호'].astype(str).str.strip()
df1_agg = df1_ss.groupby('증권번호')['수수료계'].sum().reset_index()
df1_agg['예상_지사수수료(1번파일_33%)'] = df1_agg['수수료계'] * 0.33

xls2 = pd.ExcelFile(FILE2)
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life_ss = df2_life[df2_life['제휴사'].astype(str).str.contains('삼성생명', na=False)].copy()
df2_life_ss['증권번호'] = df2_life_ss['증권번호'].astype(str).str.strip()
df2_life_ss['수수료계'] = pd.to_numeric(df2_life_ss['수수료계'], errors='coerce').fillna(0)
df2_life_agg = df2_life_ss.groupby('증권번호')['수수료계'].sum().reset_index().rename(columns={'수수료계': '실제_생명시트금액'})

sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df2_manage_ss = df2_manage[df2_manage['제휴사'].astype(str).str.contains('삼성생명', na=False)].copy()
df2_manage_ss['증권번호'] = df2_manage_ss['증권번호'].astype(str).str.strip()
fee_col = [c for c in df2_manage_ss.columns if '지사' in str(c) and ('수수료' in str(c) or '수당' in str(c))]
fee_col = fee_col[0] if fee_col else df2_manage_ss.columns[-1]
df2_manage_ss[fee_col] = pd.to_numeric(df2_manage_ss[fee_col], errors='coerce').fillna(0)
df2_manage_agg = df2_manage_ss.groupby('증권번호')[fee_col].sum().reset_index().rename(columns={fee_col: '실제_관리시트금액'})

df2_agg = pd.merge(df2_life_agg, df2_manage_agg, on='증권번호', how='outer').fillna(0)
df2_agg['실제_총수수료(2번파일)'] = df2_agg['실제_생명시트금액'] + df2_agg['실제_관리시트금액']

# 두 데이터 병합
df_comp = pd.merge(df1_agg, df2_agg, on='증권번호', how='outer').fillna(0)
df_comp['차이금액(착시오차)'] = df_comp['예상_지사수수료(1번파일_33%)'] - df_comp['실제_총수수료(2번파일)']

# [마이너스 환수 건 조건] 
# 원본(1번) 파일 수수료합계는 0보다 큰데, 
# 실제(2번) 파일 총 수수료 합계는 0보다 작은(마이너스 환수) 경우
type1_df = df_comp[(df_comp['수수료계'] > 0) & (df_comp['실제_총수수료(2번파일)'] < 0)].copy()

# 정렬 (환수액이 큰 순서대로, 즉 2번파일 금액이 작은 것부터)
type1_df = type1_df.sort_values(by='실제_총수수료(2번파일)', ascending=True)

# 컬럼명 정리 및 엑셀 저장용 구성
result_df = type1_df[['증권번호', '수수료계', '예상_지사수수료(1번파일_33%)', '실제_생명시트금액', '실제_관리시트금액', '실제_총수수료(2번파일)', '차이금액(착시오차)']].copy()
result_df.rename(columns={'수수료계': '1번원본_총수수료'}, inplace=True)

# 엑셀 저장
result_df.to_excel(OUTPUT_FILE, index=False)

print(f"✅ 추출 완료! 총 {len(result_df)}건의 증권번호가 확인되었습니다.")
print(f"📁 결과 파일 저장 위치: {OUTPUT_FILE}")

# 화면에도 일부 출력 (50개까지만)
print("\n[전체 증권번호 목록 (최대 50건 표시)]")
count = 0
for idx, row in result_df.iterrows():
    count += 1
    if count <= 50:
        print(f" {count:3d}. 증권번호: {row['증권번호']:16s} | 1번예상액: {row['예상_지사수수료(1번파일_33%)']:>10,.0f}원 | 2번실제환수액: {row['실제_총수수료(2번파일)']:>10,.0f}원 | 오차: {row['차이금액(착시오차)']:>10,.0f}원")
    
if count > 50:
    print(f" ... 등 총 {count}건 (전체 목록은 엑셀 파일을 참고하세요)")
