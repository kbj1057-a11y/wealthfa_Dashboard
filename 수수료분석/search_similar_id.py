import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("============================================================")
print("유사 증권번호 검색 ('16505862' 포함)")
print("============================================================")

xls2 = pd.ExcelFile(FILE2)

for sheet in ['생명보험', '관리수수료']:
    df = pd.read_excel(FILE2, sheet_name=sheet)
    df['증권번호'] = df['증권번호'].astype(str).str.strip()
    match = df[df['증권번호'].str.contains('16505862', na=False)]
    print(f"\n[{sheet} 시트] 검색 결과: {len(match)}건")
    if not match.empty:
        fee_col = '수수료계' if sheet == '생명보험' else ('지사수수료' if '지사수수료' in df.columns else df.columns[-1])
        print(match[['증권번호', fee_col]])
