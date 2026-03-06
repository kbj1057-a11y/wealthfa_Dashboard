import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("============================================================")
print("양쪽 시트(생명보험 + 관리수수료)에 동시 존재하는 증권번호 찾기")
print("============================================================")

xls2 = pd.ExcelFile(FILE2)

# 1. 생명보험 시트 증권번호
df_life = pd.read_excel(FILE2, sheet_name='생명보험')
df_life['증권번호'] = df_life['증권번호'].astype(str).str.strip()
life_ids = set(df_life['증권번호'].dropna())

# 2. 관리수수료 시트 증권번호 (전체)
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df_manage = pd.read_excel(FILE2, sheet_name=sheet_manage)
df_manage['증권번호'] = df_manage['증권번호'].astype(str).str.strip()
manage_ids = set(df_manage['증권번호'].dropna())

# 3. 교집합 찾기
common_ids = life_ids.intersection(manage_ids)
print(f"동시 존재 증권번호 수: {len(common_ids)} 건")

if common_ids:
    print(common_ids)
    
print("\n[사용자 제시 증권번호 '41000016505862' 확인]")
print(f"생명보험 시트 존재 여부: {'41000016505862' in life_ids}")
print(f"관리수수료 시트 존재 여부: {'41000016505862' in manage_ids}")
