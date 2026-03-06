import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*80)
print("삼성생명 [1번 문제: 마이너스 환수 차감] 심층 상세 보고")
print("="*80)

# ==========================================
# 1. 파일 로드 및 병합 (이전과 동일한 로직)
# ==========================================
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')
df1_ss = df1[df1['제휴사명'].astype(str).str.contains('삼성생명', na=False)].copy()
df1_ss['수수료계'] = pd.to_numeric(df1_ss['수수료계'], errors='coerce').fillna(0)
df1_ss['증권번호'] = df1_ss['증권번호'].astype(str).str.strip()
df1_agg = df1_ss.groupby('증권번호')['수수료계'].sum().reset_index()
df1_agg['예상_지사수수료'] = df1_agg['수수료계'] * 0.33

xls2 = pd.ExcelFile(FILE2)
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life_ss = df2_life[df2_life['제휴사'].astype(str).str.contains('삼성생명', na=False)].copy()
df2_life_ss['증권번호'] = df2_life_ss['증권번호'].astype(str).str.strip()
df2_life_ss['수수료계'] = pd.to_numeric(df2_life_ss['수수료계'], errors='coerce').fillna(0)
df2_life_agg = df2_life_ss.groupby('증권번호')['수수료계'].sum().reset_index().rename(columns={'수수료계': '상세_생명시트'})

sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df2_manage_ss = df2_manage[df2_manage['제휴사'].astype(str).str.contains('삼성생명', na=False)].copy()
df2_manage_ss['증권번호'] = df2_manage_ss['증권번호'].astype(str).str.strip()
fee_col = [c for c in df2_manage_ss.columns if '지사' in str(c) and ('수수료' in str(c) or '수당' in str(c))]
fee_col = fee_col[0] if fee_col else df2_manage_ss.columns[-1]
df2_manage_ss[fee_col] = pd.to_numeric(df2_manage_ss[fee_col], errors='coerce').fillna(0)
df2_manage_agg = df2_manage_ss.groupby('증권번호')[fee_col].sum().reset_index().rename(columns={fee_col: '상세_관리시트'})

df2_agg = pd.merge(df2_life_agg, df2_manage_agg, on='증권번호', how='outer').fillna(0)
df2_agg['실제_총수수료'] = df2_agg['상세_생명시트'] + df2_agg['상세_관리시트']

df_comp = pd.merge(df1_agg, df2_agg, on='증권번호', how='outer').fillna(0)
df_comp['차이금액'] = df_comp['예상_지사수수료'] - df_comp['실제_총수수료']

# ==========================================
# 2. 유형 1 (마이너스 환수 건 191건 필터링)
# ==========================================
# 정의: 1번 원본 수수료는 플러스(돈 받을게 있음)인데, 2번 최종 정산금액은 마이너스(돈을 뱉어냄)인 경우
type1_df = df_comp[(df_comp['수수료계'] > 0) & (df_comp['실제_총수수료'] < 0)].copy()

print(f"\n[현황 파악]")
print(f"  - 해당 건수: 총 {len(type1_df)} 건")

# 이 191건 때문에 회사가 얼마나 손해볼 뻔(예상치 대비 차이) 했는지 합계 계산
# 예상 33% 몫이었던 금액
total_expected = type1_df['예상_지사수수료'].sum()
# 실제로 회사에서 빼간 (환수당한) 금액
total_actual = type1_df['실제_총수수료'].sum()
# 오차 규모 (만약 1번 기준으로 계산했다면 회계상 펑크날 금액)
total_error = type1_df['차이금액'].sum()

print(f"  - 1번(원본) 기준 우리가 받을 줄 알았던 지사수수료(33%) 총액: {total_expected:,.0f} 원")
print(f"  - 2번(상세) 기준 우리가 실제로 삼성생명에 토해낸(환수된) 총액: {total_actual:,.0f} 원")
print(f"  ▶ 1번 엑셀의 숫자만 믿었다면 발생했을 [착시 오차 총액]: {total_error:,.0f} 원")

print("\n" + "="*80)
print("[환수 금액(피해액)이 가장 큰 TOP 5 증권번호 상세 분석]")
print("="*80)

top5 = type1_df.sort_values(by='실제_총수수료').head(5) # 실제 환수액이 마이너스로 젤 큰 순

for idx, row in top5.iterrows():
    # 해당 증권번호의 원본 데이터들(계약일자, 회차 등)을 1번 파일 원본(df1_ss)에서 모두 가져오기
    source_rows = df1_ss[df1_ss['증권번호'] == row['증권번호']]
    
    print(f"\n■ 증권번호: {row['증권번호']}")
    
    # 1. 1번 파일에서는 이 건을 어떻게 기록하고 있었길래 이런 오류가?
    print("  [1번 파일 기록]")
    print(f"    - 총 원 수수료: +{row['수수료계']:,.0f} 원 (우리가 수당 발생했다고 인지함)")
    print(f"    - 33% 공식 기대수익: +{row['예상_지사수수료']:,.0f} 원")
    
    # 원본 파일에 찍힌 세부 수당 내역 확인 (어떤 항목에 돈이 들어와 있었는지)
    # df1_ss 에는 1, 2, 3.. 37 회차 수수료 컬럼들이 있음. 0 이상인 항목만 나열
    fee_details = []
    for _, s_row in source_rows.iterrows():
        # 납입회차 1~37 컬럼명 찾기
        for i in range(1, 40):
            col_name = str(i)
            if col_name in s_row.index and pd.to_numeric(s_row[col_name], errors='coerce') > 0:
                fee_details.append(f"{i}회차={s_row[col_name]:,.0f}원")
        # 혹시 '초회', '1차년' 등 주요 요약 항목 검사
        for c in ['초회', '1차년', '2차년', '3차년']:
            if c in s_row.index:
                val = pd.to_numeric(s_row[c], errors='coerce')
                if val > 0:
                    fee_details.append(f"[{c}] {val:,.0f}원")
                    
    # 중복 제거 및 깔끔하게 출력
    fee_details = list(set(fee_details))
    if fee_details:
         print(f"    - 원본에 적힌 지급 명세: {', '.join(fee_details[:5])} ...")

    # 2. 2번 파일에서는 왜 마이너스로 정산했을까?
    print("  [2번 파일 정산 결과]")
    print(f"    - 실제 지사수수료 정산액: {row['실제_총수수료']:,.0f} 원 (마이너스 환수!)")
    
    # 발생한 오차
    print(f"  ▶ 분석 결과: 1번 파일에는 '+수당'으로 적혀있으나, 과거 지급분 환수 등의 사유로 삼성생명은 '{row['실제_총수수료']:,.0f}원'을 차감했습니다.")
    print(f"     (이 증권 1건에서 터진 계산 오차만 {row['차이금액']:,.0f}원 입니다)")
    print("-" * 60)
