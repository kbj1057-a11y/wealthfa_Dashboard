import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*60)
print("미래에셋생명 수수료 불일치 심층 분석")
print("="*60)

# ==========================================
# 1. 파일 1 (생손보통합) 데이터 준비 - 미래에셋생명만
# ==========================================
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')
df1_mirae = df1[df1['제휴사명'].astype(str).str.contains('미래에셋', na=False)].copy()

df1_mirae['수수료계'] = pd.to_numeric(df1_mirae['수수료계'], errors='coerce').fillna(0)
df1_mirae['증권번호'] = df1_mirae['증권번호'].astype(str).str.strip()

# 미래에셋생명의 1번 파일 총 수수료계
A_mirae = df1_mirae['수수료계'].sum()
calc_A_mirae = A_mirae * 0.33  # A * 0.35 - (A * 0.02)

print(f"\n[1] 파일 1 (포털 다운로드 원본)")
print(f"  - 미래에셋생명 총 수수료계 (A) : {A_mirae:,.0f} 원")
print(f"  - 공식 계산값 (A * 0.33)       : {calc_A_mirae:,.0f} 원")

# 증권번호별 집계
df1_mirae_agg = df1_mirae.groupby('증권번호')['수수료계'].sum().reset_index()
df1_mirae_agg['예상_지사수수료'] = df1_mirae_agg['수수료계'] * 0.33

# ==========================================
# 2. 파일 2 (지사장 상세) 데이터 준비 - 미래에셋생명만
# ==========================================
xls2 = pd.ExcelFile(FILE2)

# 2-1) 생명보험 시트에서 미래에셋생명
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life_mirae = df2_life[df2_life['제휴사'].astype(str).str.contains('미래에셋', na=False)].copy()
df2_life_mirae['증권번호'] = df2_life_mirae['증권번호'].astype(str).str.strip()
df2_life_mirae['수수료계'] = pd.to_numeric(df2_life_mirae['수수료계'], errors='coerce').fillna(0)
life_sum_mirae = df2_life_mirae['수수료계'].sum()

# 2-2) 관리수수료 시트에서 미래에셋생명
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df2_manage_mirae = df2_manage[df2_manage['제휴사'].astype(str).str.contains('미래에셋', na=False)].copy()
df2_manage_mirae['증권번호'] = df2_manage_mirae['증권번호'].astype(str).str.strip()

fee_col = '지사수수료' if '지사수수료' in df2_manage_mirae.columns else df2_manage_mirae.columns[-1]
df2_manage_mirae[fee_col] = pd.to_numeric(df2_manage_mirae[fee_col], errors='coerce').fillna(0)
manage_sum_mirae = df2_manage_mirae[fee_col].sum()

file2_total_mirae = life_sum_mirae + manage_sum_mirae

print(f"\n[2] 파일 2 (최종 정산 상세)")
print(f"  - [생명보험] 시트 수수료계 : {life_sum_mirae:,.0f} 원")
print(f"  - [관리수수료] 시트 지사수수료 : {manage_sum_mirae:,.0f} 원")
print(f"  => 파일 2 최종 합계 : {file2_total_mirae:,.0f} 원")

print(f"\n[차이 종합] 1번 예상({calc_A_mirae:,.0f}) vs 2번 실제({file2_total_mirae:,.0f}) = {calc_A_mirae - file2_total_mirae:,.0f} 원 차이")

# 증권번호별 집계
df2_life_agg_mirae = df2_life_mirae.groupby('증권번호')['수수료계'].sum().reset_index().rename(columns={'수수료계': '상세_생명시트'})
df2_manage_agg_mirae = df2_manage_mirae.groupby('증권번호')[fee_col].sum().reset_index().rename(columns={fee_col: '상세_관리시트'})
df2_mirae_agg = pd.merge(df2_life_agg_mirae, df2_manage_agg_mirae, on='증권번호', how='outer').fillna(0)
df2_mirae_agg['파일2_총수수료'] = df2_mirae_agg['상세_생명시트'] + df2_mirae_agg['상세_관리시트']

# ==========================================
# 3. 개별 증권번호 대조 및 심층 분석
# ==========================================
compare_mirae = pd.merge(df1_mirae_agg, df2_mirae_agg, on='증권번호', how='outer').fillna(0)
compare_mirae['차이금액'] = compare_mirae['예상_지사수수료'] - compare_mirae['파일2_총수수료']

# 차이가 없는(거의 없는) 정상 건과 차이가 큰 건 분리
compare_mirae['실제적용요율'] = (compare_mirae['파일2_총수수료'] / compare_mirae['수수료계'].replace(0, pd.NA)).fillna(0) * 100

# 소수점 오차가 아닌 유의미한 차이(10원 초과)가 있는 계약 찾기
diff_mirae = compare_mirae[compare_mirae['차이금액'].abs() > 10].sort_values(by='차이금액', key=abs, ascending=False)

print("\n" + "="*60)
if len(diff_mirae) > 0:
    print(f"미래에셋생명 차이 발생 계약 분석 (총 {len(diff_mirae)}건 발견)")
    print("="*60)
    for _, row in diff_mirae.iterrows():
        print(f"[증권번호: {row['증권번호']}]")
        print(f"  - 1번 원수수료: {row['수수료계']:,.0f} 원")
        print(f"  - 1번 공식적용: {row['예상_지사수수료']:,.0f} 원 (33%)")
        print(f"  - 2번 실제지급: {row['파일2_총수수료']:,.0f} 원 (생명:{row['상세_생명시트']:,.0f} + 관리:{row['상세_관리시트']:,.0f})")
        print(f"  - 실제 적용요율: {row['실제적용요율']:.1f}%")
        print(f"  - 차이: {row['차이금액']:,.0f} 원")
        print("-" * 40)
else:
    print("미래에셋생명 계약 분석 결과: 모든 계약이 산식(33%)과 정확히 일치합니다!")
    print("="*60)
