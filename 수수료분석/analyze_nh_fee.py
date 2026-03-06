import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*60)
print("농협생명 수수료 불일치 심층 분석")
print("="*60)

# ==========================================
# 1. 파일 1 (생손보통합) 데이터 준비 - 농협생명만
# ==========================================
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')
df1_nh = df1[df1['제휴사명'].astype(str).str.contains('농협생명', na=False)].copy()

df1_nh['수수료계'] = pd.to_numeric(df1_nh['수수료계'], errors='coerce').fillna(0)
df1_nh['증권번호'] = df1_nh['증권번호'].astype(str).str.strip()

# 농협생명의 1번 파일 총 수수료계
A_nh = df1_nh['수수료계'].sum()
calc_A_nh = A_nh * 0.33  # A * 0.35 - (A * 0.02)

print(f"\n[1] 파일 1 (포털 다운로드 원본)")
print(f"  - 농협생명 총 수수료계 (A) : {A_nh:,.0f} 원")
print(f"  - 공식 계산값 (A * 0.33)   : {calc_A_nh:,.0f} 원")

# 증권번호별 집계
df1_nh_agg = df1_nh.groupby('증권번호')['수수료계'].sum().reset_index()
df1_nh_agg['예상_지사수수료'] = df1_nh_agg['수수료계'] * 0.33

# ==========================================
# 2. 파일 2 (지사장 상세) 데이터 준비 - 농협생명만
# ==========================================
xls2 = pd.ExcelFile(FILE2)

# 2-1) 생명보험 시트에서 농협생명
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life_nh = df2_life[df2_life['제휴사'].astype(str).str.contains('농협생명', na=False)].copy()
df2_life_nh['증권번호'] = df2_life_nh['증권번호'].astype(str).str.strip()
df2_life_nh['수수료계'] = pd.to_numeric(df2_life_nh['수수료계'], errors='coerce').fillna(0)
life_sum_nh = df2_life_nh['수수료계'].sum()

# 2-2) 관리수수료 시트에서 농협생명
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df2_manage_nh = df2_manage[df2_manage['제휴사'].astype(str).str.contains('농협생명', na=False)].copy()
df2_manage_nh['증권번호'] = df2_manage_nh['증권번호'].astype(str).str.strip()

fee_col = '지사수수료' if '지사수수료' in df2_manage_nh.columns else df2_manage_nh.columns[-1]
df2_manage_nh[fee_col] = pd.to_numeric(df2_manage_nh[fee_col], errors='coerce').fillna(0)
manage_sum_nh = df2_manage_nh[fee_col].sum()

file2_total_nh = life_sum_nh + manage_sum_nh

print(f"\n[2] 파일 2 (최종 정산 상세)")
print(f"  - [생명보험] 시트 수수료계 : {life_sum_nh:,.0f} 원")
print(f"  - [관리수수료] 시트 지사수수료 : {manage_sum_nh:,.0f} 원")
print(f"  => 파일 2 최종 합계 : {file2_total_nh:,.0f} 원")

print(f"\n[차이 종합] 1번 예상({calc_A_nh:,.0f}) vs 2번 실제({file2_total_nh:,.0f}) = {calc_A_nh - file2_total_nh:,.0f} 원 차이")

# 증권번호별 집계
df2_life_agg_nh = df2_life_nh.groupby('증권번호')['수수료계'].sum().reset_index().rename(columns={'수수료계': '상세_생명시트'})
df2_manage_agg_nh = df2_manage_nh.groupby('증권번호')[fee_col].sum().reset_index().rename(columns={fee_col: '상세_관리시트'})
df2_nh_agg = pd.merge(df2_life_agg_nh, df2_manage_agg_nh, on='증권번호', how='outer').fillna(0)
df2_nh_agg['파일2_총수수료'] = df2_nh_agg['상세_생명시트'] + df2_nh_agg['상세_관리시트']

# ==========================================
# 3. 개별 증권번호 대조 및 심층 분석
# ==========================================
compare_nh = pd.merge(df1_nh_agg, df2_nh_agg, on='증권번호', how='outer').fillna(0)
compare_nh['차이금액'] = compare_nh['예상_지사수수료'] - compare_nh['파일2_총수수료']

# 차이가 없는(거의 없는) 정상 건과 차이가 큰 건 분리
compare_nh['실제적용요율'] = (compare_nh['파일2_총수수료'] / compare_nh['수수료계'].replace(0, pd.NA)).fillna(0) * 100

print("\n" + "="*60)
print("농협생명 계약 분석 (전체 리스트)")
print("="*60)
for _, row in compare_nh.iterrows():
    print(f"[증권번호: {row['증권번호']}]")
    print(f"  - 1번 원수수료: {row['수수료계']:,.0f} 원")
    print(f"  - 1번 공식적용: {row['예상_지사수수료']:,.0f} 원 (33%)")
    print(f"  - 2번 실제지급: {row['파일2_총수수료']:,.0f} 원 (생명:{row['상세_생명시트']:,.0f} + 관리:{row['상세_관리시트']:,.0f})")
    print(f"  - 실제 적용요율: {row['실제적용요율']:.1f}%")
    print(f"  - 차이: {row['차이금액']:,.0f} 원")
    print("-" * 40)
