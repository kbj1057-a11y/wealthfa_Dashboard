import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"
CONTRACT_FILE = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)\20260227_144604_계약일자별조회.xlsx"

df_master = pd.read_excel(FILE_MASTER, sheet_name="RAWDATA")
df_contract = pd.read_excel(CONTRACT_FILE)

# 마스터 파일에서 계약일자 최신/최대값 확인
print("=== 마스터 파일의 계약일자 최솟값/최댓값 ===")
master_dates = pd.to_datetime(df_master['계약일자'], errors='coerce')
print(f"최솟값: {master_dates.min()}")
print(f"최댓값: {master_dates.max()}")
print(f"총 계약수: {len(df_master)}")

# 계약 파일의 ID 목록
# 계약 파일 증권번호(14번 인덱스 = 'y' 컬럼)
col_id_contract = df_contract.columns[14]
contract_ids = set(df_contract[col_id_contract].astype(str).str.strip().unique())

# 마스터 파일의 증권번호
master_ids = set(df_master['증권번호'].astype(str).str.strip().unique())

# 계약 파일에는 있지만 마스터에 없는 건 (신규 계약)
new_contracts = contract_ids - master_ids
print(f"\n=== 계약 파일에만 있는 신규 계약 (미반영) ===")
print(f"신규 계약 수: {len(new_contracts)}")
for cid in sorted(new_contracts):
    row = df_contract[df_contract[col_id_contract].astype(str).str.strip() == cid].iloc[0]
    print(f"  {cid} | FC: {row['FC명']} | 제휴사: {row['제휴사']} | 계약일: {row['계약일자']}")

# 계약 파일의 최신 날짜 확인
contract_dates = pd.to_datetime(df_contract['계약일자'], errors='coerce')
print(f"\n=== 계약 파일 날짜 범위 ===")
print(f"최솟값: {contract_dates.min()}")
print(f"최댓값: {contract_dates.max()}")
print(f"총 건수: {len(df_contract)}")
