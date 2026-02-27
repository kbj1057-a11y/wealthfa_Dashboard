import pandas as pd
import glob
import os

DIR_FEE = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"

def get_latest_file(directory, pattern="*.xlsx"):
    files = glob.glob(os.path.join(directory, pattern))
    files = [f for f in files if not os.path.basename(f).startswith("~$")]
    if not files: return None
    return max(files, key=os.path.getctime)

latest_fee = get_latest_file(DIR_FEE)
latest_contract = get_latest_file(DIR_CONTRACT)

print(f"Fee File: {latest_fee}")
if latest_fee:
    df = pd.read_excel(latest_fee)
    print(f"Fee Columns: {df.columns.tolist()}")

print(f"\nContract File: {latest_contract}")
if latest_contract:
    df = pd.read_excel(latest_contract)
    print(f"Contract Columns: {df.columns.tolist()}")

print(f"\nMaster File: {FILE_MASTER}")
if os.path.exists(FILE_MASTER):
    df = pd.read_excel(FILE_MASTER, sheet_name="RAWDATA")
    print(f"Master Columns: {df.columns.tolist()}")
