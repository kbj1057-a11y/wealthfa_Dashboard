import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"
FILE_MERGED = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx"

TARGET_ID = "41000016505862"

print(f"============================================================")
print(f"증권번호 [{TARGET_ID}] 정밀 추적")
print(f"============================================================")

print("\n1. 원본 1번 파일 (생손보통합) 확인")
df1 = pd.read_excel(FILE1, sheet_name='생명보험사_202602')
df1['증권번호'] = df1['증권번호'].astype(str).str.strip()
target_df1 = df1[df1['증권번호'] == TARGET_ID]
print(f"  - 1번 파일 조회 결과: {len(target_df1)}건")
if not target_df1.empty:
    print(f"  - 수수료계: {target_df1['수수료계'].tolist()}")

print("\n2. 원본 2번 파일 (상세내역) 확인")
xls2 = pd.ExcelFile(FILE2)

# 생명보험 시트 확인
df2_life = pd.read_excel(FILE2, sheet_name='생명보험')
df2_life['증권번호'] = df2_life['증권번호'].astype(str).str.strip()
target_df2_life = df2_life[df2_life['증권번호'] == TARGET_ID]
print(f"  - [생명보험 시트] 조회 결과: {len(target_df2_life)}건")
if not target_df2_life.empty:
    print(f"  - 수수료계: {target_df2_life['수수료계'].tolist()}")

# 관리수수료 시트 확인
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df2_manage['증권번호'] = df2_manage['증권번호'].astype(str).str.strip()
target_df2_manage = df2_manage[df2_manage['증권번호'] == TARGET_ID]
print(f"  - [{sheet_manage} 시트] 조회 결과: {len(target_df2_manage)}건")
if not target_df2_manage.empty:
    fee_col = '지사수수료' if '지사수수료' in df2_manage.columns else df2_manage.columns[-1]
    print(f"  - {fee_col}: {target_df2_manage[fee_col].tolist()}")

print("\n3. 최종 병합본 파일 확인")
df_merged = pd.read_excel(FILE_MERGED, sheet_name='생명보험사_202602')
df_merged['증권번호'] = df_merged['증권번호'].astype(str).str.strip()
target_merged = df_merged[df_merged['증권번호'] == TARGET_ID]
print(f"  - [최종 병합본] 조회 결과: {len(target_merged)}건")
if not target_merged.empty:
    print(f"  - 지사수수료 기록값: {target_merged['지사수수료'].values[0]}")
    if '분담금' in target_merged.columns:
        print(f"  - 분담금 기록값: {target_merged['분담금'].values[0]}")
