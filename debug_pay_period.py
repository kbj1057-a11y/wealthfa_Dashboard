import pandas as pd
import glob
import os

DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"

def get_latest_file(directory, pattern="*.xlsx"):
    files = glob.glob(os.path.join(directory, pattern))
    files = [f for f in files if not os.path.basename(f).startswith("~$")]
    if not files: return None
    return max(files, key=os.path.getctime)

latest_contract = get_latest_file(DIR_CONTRACT)

print(f"--- [파일 정보] ---")
print(f"최신 계약 파일: {latest_contract}")
print(f"마스터 파일: {FILE_MASTER}")

if latest_contract and os.path.exists(FILE_MASTER):
    df_contract = pd.read_excel(latest_contract)
    df_master = pd.read_excel(FILE_MASTER, sheet_name="RAWDATA")
    
    print(f"\n--- [원본 컬럼 상세] ---")
    print(f"계약 파일 컬럼: {df_contract.columns.tolist()}")
    print(f"마스터 파일 컬럼: {df_master.columns.tolist()}")
    
    # 납입기간 관련 컬럼 검색
    pay_cols_contract = [c for c in df_contract.columns if '납입' in str(c) or '기간' in str(c)]
    pay_cols_master = [c for c in df_master.columns if '납입' in str(c) or '기간' in str(c)]
    
    print(f"\n--- [검색된 후보 컬럼] ---")
    print(f"계약 파일 후보: {pay_cols_contract}")
    print(f"마스터 파일 후보: {pay_cols_master}")
    
    # 증권번호 컬럼 확인
    id_cols_contract = [c for c in df_contract.columns if '증권' in str(c) or '번호' in str(c)]
    id_cols_master = [c for c in df_master.columns if '증권' in str(c) or '번호' in str(c)]
    
    print(f"\n--- [ID 컬럼 확인] ---")
    print(f"계약 ID 후보: {id_cols_contract}")
    print(f"마스터 ID 후보: {id_cols_master}")
    
    # 샘플 데이터 비교 (만약 ID 컬럼이 있다면)
    if id_cols_contract and id_cols_master:
        cid = id_cols_contract[0]
        mid = id_cols_master[0]
        
        # 계약 파일에는 있는데 마스터에는 없는 번호가 있는지 확인
        c_ids = set(df_contract[cid].astype(str).str.strip().unique())
        m_ids = set(df_master[mid].astype(str).str.strip().unique())
        
        common = c_ids.intersection(m_ids)
        print(f"\n--- [데이터 매칭 확인] ---")
        print(f"공통 증권번호 개수: {len(common)}개")
        
        if pay_cols_contract:
            p_col = pay_cols_contract[0]
            print(f"\n계약 파일 샘플 (ID, {p_col}):")
            print(df_contract[[cid, p_col]].head(10))
            
            non_empty_pay = df_contract[df_contract[p_col].notna()]
            print(f"계약 파일 내 {p_col} 데이터가 있는 행 수: {len(non_empty_pay)}")
