import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"

def get_latest_file(directory, pattern="*.xlsx"):
    files = glob.glob(os.path.join(directory, pattern))
    files = [f for f in files if not os.path.basename(f).startswith("~$")]
    if not files: return None
    return max(files, key=os.path.getctime)

latest_contract = get_latest_file(DIR_CONTRACT)
print(f"최신 계약 파일: {latest_contract}")

df_contract = pd.read_excel(latest_contract)

# 14번 인덱스 = 증권번호(y컬럼), 28번 인덱스 = 날짜 컬럼
# 계약 파일에서 '계약일자' 컬럼 찾기
print(f"\n계약 파일 컬럼 수: {len(df_contract.columns)}")
print(f"계약 파일 행 수: {len(df_contract)}")

# 날짜 관련 컬럼 찾기
for i, col in enumerate(df_contract.columns):
    sample = df_contract.iloc[0, i]
    print(f"Index {i}: {col} | 샘플값: {sample}")
