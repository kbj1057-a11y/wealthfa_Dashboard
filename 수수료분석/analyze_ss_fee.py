import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*60)
print("삼성생명 수수료 불일치 심층/유형 분석")
print("="*60)

# ==========================================
# 1. 파일 1 (포털 다운로드 원본) - 삼성생명
# ==========================================
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')
df1_ss = df1[df1['제휴사명'].astype(str).str.contains('삼성생명', na=False)].copy()

df1_ss['수수료계'] = pd.to_numeric(df1_ss['수수료계'], errors='coerce').fillna(0)
df1_ss['증권번호'] = df1_ss['증권번호'].astype(str).str.strip()

# 원본 증권번호별 수수료 합계
df1_agg = df1_ss.groupby('증권번호')['수수료계'].sum().reset_index()
df1_agg['예상_지사수수료'] = df1_agg['수수료계'] * 0.33

# ==========================================
# 2. 파일 2 (정산 상세 엑셀) - 삼성생명
# ==========================================
xls2 = pd.ExcelFile(FILE2)

# 2-1) 생명보험 시트
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life_ss = df2_life[df2_life['제휴사'].astype(str).str.contains('삼성생명', na=False)].copy()
df2_life_ss['증권번호'] = df2_life_ss['증권번호'].astype(str).str.strip()
df2_life_ss['수수료계'] = pd.to_numeric(df2_life_ss['수수료계'], errors='coerce').fillna(0)
df2_life_agg = df2_life_ss.groupby('증권번호')['수수료계'].sum().reset_index().rename(columns={'수수료계': '상세_생명시트'})

# 2-2) 관리수수료 시트
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df2_manage_ss = df2_manage[df2_manage['제휴사'].astype(str).str.contains('삼성생명', na=False)].copy()
df2_manage_ss['증권번호'] = df2_manage_ss['증권번호'].astype(str).str.strip()

fee_col = '지사수수료' if '지사수수료' in df2_manage_ss.columns else df2_manage_ss.columns[-1]
df2_manage_ss[fee_col] = pd.to_numeric(df2_manage_ss[fee_col], errors='coerce').fillna(0)
df2_manage_agg = df2_manage_ss.groupby('증권번호')[fee_col].sum().reset_index().rename(columns={fee_col: '상세_관리시트'})

# 파일 2 (생명 + 관리) 병합
df2_agg = pd.merge(df2_life_agg, df2_manage_agg, on='증권번호', how='outer').fillna(0)
df2_agg['실제_총수수료'] = df2_agg['상세_생명시트'] + df2_agg['상세_관리시트']

# ==========================================
# 3. 양쪽 파일 병합 및 차이 요인 분류
# ==========================================
df_comp = pd.merge(df1_agg, df2_agg, on='증권번호', how='outer').fillna(0)
df_comp['차이금액'] = df_comp['예상_지사수수료'] - df_comp['실제_총수수료']

# 차이가 없는(거의 없는) 건 제거 (10원 기준)
df_diff = df_comp[df_comp['차이금액'].abs() > 10].copy()

# -----------------
# 오류 유형 분류 로직
# -----------------
def categorize(row):
    v1_raw = row['수수료계']            # 1번 파일 총 수수료
    v1_est = row['예상_지사수수료']     # 1번 파일 예상 (33%)
    v2_life = row['상세_생명시트']      # 2번 생명 시트
    v2_manage = row['상세_관리시트']    # 2번 관리 시트
    v2_total = row['실제_총수수료']      # 2번 전체
    sec_no = row['증권번호']
    
    # 1. 추가 보너스/시책 (.0 등) - 1번 파일에는 0원(또는 아예 없음)인데 2번 파일에서 지급됨
    if v1_raw == 0 and v2_total > 0:
        if '.0' in sec_no:
            return "유형1(보너스등): 증권번호 뒤 '.0' 추가 지급건 (원본엑셀=0원)"
        return "유형1(보너스등): 원본 엑셀에 없는 추가 지급건"
    
    # 2. 마이너스 환수 - 2번 파일에서 수당이 마이너스(-)로 차감됨
    if v2_total < 0:
        if v1_raw > 0:
            return "유형2(마이너스환수): 원본엑셀은 플러스(+)이나, 정산시 미유지 등의 사유로 차감(-) 됨"
        return "유형2(마이너스환수): 원본과 정산 모두 마이너스이나 금액 상이"
    
    # 3. 요율 차이 (98% 등) - 1번 파일에 데이터는 있으나 33% 룰이 아닌 다른 요율
    if v1_raw > 0 and v2_total > 0:
        ratio = (v2_total / v1_raw) * 100
        # 33% 근처가 아닌 경우
        if abs(ratio - 33.0) > 3.0: 
            return f"유형3(요율특례): 33%가 아닌 별도요율 적용건 (적용률: {ratio:.1f}%)"
            
    # 그 외 미분류
    return "유형4(기타불일치): 복합적인 요인"

df_diff['오류유형'] = df_diff.apply(categorize, axis=1)

# ==========================================
# 4. 결과 요약 출력
# ==========================================
print(f"\n[삼성생명 불일치 데이터 개요]")
summary = df_diff['오류유형'].value_counts()
for name, cnt in summary.items():
    print(f"  - {name}: {cnt}건")

print("\n" + "="*60)
print("[유형별 대표 케이스 3건씩 확인]")
print("="*60)

for cat in df_diff['오류유형'].unique():
    subset = df_diff[df_diff['오류유형'] == cat].sort_values(by='차이금액', key=abs, ascending=False).head(3)
    print(f"\n■ {cat} (대표 샘플)")
    for _, r in subset.iterrows():
        print(f"  - 증권번호: {r['증권번호']}")
        print(f"      1번 엑셀: 원수수료 {r['수수료계']:,.0f} 원 -> 예상액 {r['예상_지사수수료']:,.0f} 원")
        print(f"      2번 엑셀: 실지급액 {r['실제_총수수료']:,.0f} 원 (생명 {r['상세_생명시트']:,.0f} + 관리 {r['상세_관리시트']:,.0f})")
        print(f"      => 차이금액: {r['차이금액']:,.0f} 원")
