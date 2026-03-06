import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*60)
print("생명보험사 수수료 금액 불일치 원인 분석")
print("="*60)

# ==========================================
# 1. 파일 1 (생손보통합) 데이터 준비
# ==========================================
print("\n[1] 파일 1 (통합 파일) 데이터 로드 중...")
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')

# 수수료계 숫자 변환
df1['수수료계'] = pd.to_numeric(df1['수수료계'], errors='coerce').fillna(0)
df1['증권번호'] = df1['증권번호'].astype(str).str.strip()
df1['제휴사명'] = df1['제휴사명'].astype(str).str.strip()

# A: 총 수수료계
A = df1['수수료계'].sum()
# 공식: A * 0.35 - (A * 0.02) = A * 0.33
calc_A = A * 0.35 - (A * 0.02)

print(f"  - 1번 파일 총 수수료계 (A) : {A:,.0f} 원")
print(f"  - 1번 파일 공식 계산값 [A * 0.35 - (A * 0.02)] : {calc_A:,.0f} 원")

# 증권번호별 수수료 및 계산값 집계
df1_agg = df1.groupby(['증권번호', '제휴사명'])['수수료계'].sum().reset_index()
df1_agg['예상_지사수수료'] = df1_agg['수수료계'] * 0.33

# ==========================================
# 2. 파일 2 (상세내역) 데이터 준비
# ==========================================
print("\n[2] 파일 2 (지사장 상세 파일) 데이터 로드 중...")
xls2 = pd.ExcelFile(FILE2)

# 2-1) 생명보험 시트
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life['증권번호'] = df2_life['증권번호'].astype(str).str.strip()
df2_life['수수료계'] = pd.to_numeric(df2_life['수수료계'], errors='coerce').fillna(0)
life_sum = df2_life['수수료계'].sum()
print(f"  - [생명보험] 시트 수수료계 총합: {life_sum:,.0f} 원")

# 2-2) 관리수수료 시트
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)

# 생명보험사만 필터
df2_manage_life = df2_manage[df2_manage['제휴사'].astype(str).str.contains('생명', na=False)].copy()
df2_manage_life['증권번호'] = df2_manage_life['증권번호'].astype(str).str.strip()

# '지사수수료' 관련된 컬럼 찾기
possible_fee_cols = [c for c in df2_manage_life.columns if '지사' in str(c) and ('수수료' in str(c) or '수당' in str(c))]
fee_col = '지사수수료' if '지사수수료' in df2_manage_life.columns else None
if not fee_col and possible_fee_cols:
    fee_col = possible_fee_cols[0]
elif not fee_col:
    # 혹시 이름이 다를경우 수수료계 등을 찾음
    fallback = [c for c in df2_manage_life.columns if '수수료' in str(c) or '지급' in str(c) or '합계' in str(c)]
    fee_col = fallback[0] if fallback else df2_manage_life.columns[-1]

print(f"  - [관리수수료] 시트 금액 타겟 컬럼 자동선택: '{fee_col}'")

df2_manage_life[fee_col] = pd.to_numeric(df2_manage_life[fee_col], errors='coerce').fillna(0)
manage_sum = df2_manage_life[fee_col].sum()
print(f"  - [관리수수료] 시트(생명) 지사수수료 총합: {manage_sum:,.0f} 원")

# 2번 파일 총합
file2_total = life_sum + manage_sum
print(f"\n  => 2번 파일 합계 (생명보험 + 관리수수료) : {file2_total:,.0f} 원")

# 증권번호별 집계 병합 (생명보험 + 관리수수료)
df2_life_agg = df2_life.groupby(['증권번호', '제휴사'])['수수료계'].sum().reset_index().rename(columns={'수수료계': '상세_수수료계', '제휴사':'제휴사명'})
df2_manage_agg = df2_manage_life.groupby(['증권번호', '제휴사'])[fee_col].sum().reset_index().rename(columns={fee_col: '상세_지사수수료', '제휴사':'제휴사명'})

# 증권번호 기준으로 2번파일 데이터 병합
df2_agg = pd.merge(df2_life_agg, df2_manage_agg, on=['증권번호', '제휴사명'], how='outer').fillna(0)
df2_agg['파일2_총수수료'] = df2_agg['상세_수수료계'] + df2_agg['상세_지사수수료']

# ==========================================
# 3. 데이터 대조 및 불일치 원인 분석
# ==========================================
print("\n" + "="*60)
print("차이 금액 종합 분석")
print("="*60)
diff_amount = calc_A - file2_total

print(f"  1번 파일 예상 지사수수료 : {calc_A:,.0f} 원")
print(f"  2번 파일 실제 지사수수료 : {file2_total:,.0f} 원")
print(f"  ---------------------------------------------------")
print(f"  차이 (1번 - 2번)         : {diff_amount:,.0f} 원")

# 증권번호 별 1, 2번 파일 병합 대조
compare_df = pd.merge(df1_agg, df2_agg, on='증권번호', how='outer').fillna(0)
compare_df['제휴사'] = compare_df['제휴사명_x'].where(compare_df['제휴사명_x'] != 0, compare_df['제휴사명_y'])
compare_df['차이금액'] = compare_df['예상_지사수수료'] - compare_df['파일2_총수수료']
compare_df['차이금액_절대값'] = compare_df['차이금액'].abs()

# 불일치가 있는 건만 추출 (소수점 단수 차이 등 10원 미만은 제외)
diff_df = compare_df[compare_df['차이금액_절대값'] > 10].sort_values(by='차이금액_절대값', ascending=False)

print(f"\n[불일치 분석 1] 회사별 차이 금액 합계")
company_diff = diff_df.groupby('제휴사')['차이금액'].sum().reset_index()
for _, row in company_diff.iterrows():
    print(f"  - {row['제휴사']:<10} : {row['차이금액']:,.0f} 원 차이 발생")

print(f"\n[불일치 분석 2] 차이가 큰 개별 증권번호 TOP 10")
for i, row in diff_df.head(10).iterrows():
    print(f"  - 증권번호: {row['증권번호']} ({row['제휴사']})")
    print(f"      1번 원수수료: {row['수수료계']:,.0f}원 -> (예상 33%): {row['예상_지사수수료']:,.0f}원")
    print(f"      2번 상세수행: {row['파일2_총수수료']:,.0f}원 (생명:{row['상세_수수료계']:,.0f} + 관리:{row['상세_지사수수료']:,.0f})")
    print(f"      차이: {row['차이금액']:,.0f}원")

# 추가 분석: 혹시 수수료가 (-)인 항목 처리의 차이, 또는 특정 항목(유지율 환수 등) 제외 여부
print("\n[불일치 가설]")
print("1. 특정 회사(예: 삼성생명)의 요율이 33%가 아닌 별도 요율로 계산되었을 가능성")
print("2. 1번 파일의 마이너스(-) 환수 건이 2번 파일에서 다르게 집계되었을 가능성")
print("3. 관리수수료 대상에서 제외되는 특정 계약 건(본인계약 등) 존재 가능성")
print("4. 1번 파일 '수수료계' 외에 인센티브(시상) 항목이 2번 파일에 추가/제외 되었을 가능성")

