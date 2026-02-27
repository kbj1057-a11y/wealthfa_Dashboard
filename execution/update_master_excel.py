import pandas as pd
import glob
import os
import shutil
import datetime
import sys

# 한글 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# 경로 설정
DIR_FEE = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"
SHEET_NAME = "RAWDATA"

def get_latest_file(directory, pattern="*.xlsx"):
    files = glob.glob(os.path.join(directory, pattern))
    files = [f for f in files if not os.path.basename(f).startswith("~$")]
    if not files: return None
    return max(files, key=os.path.getctime)

def backup_master_file():
    if not os.path.exists(FILE_MASTER): return
    backup_dir = os.path.join(os.path.dirname(FILE_MASTER), "backup")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}_{os.path.basename(FILE_MASTER)}")
    shutil.copy2(FILE_MASTER, backup_path)
    print(f"📦 [백업] 원본 파일 백업 완료: {os.path.basename(backup_path)}")

def get_contract_id_column(df):
    """계약 파일에서 증권번호(인덱스 14번) 컬럼을 찾음"""
    if df.shape[1] > 14:
        return df.columns[14]
    # 폴백: '증권'이나 'y'가 포함된 컬럼
    for col in df.columns:
        if '증권' in str(col) or str(col).lower() == 'y':
            return col
    return df.columns[0]

def update_master():
    print("======== 26년 업적/수수료 통계 업데이트 (정비 버전) ========")
    
    latest_fee = get_latest_file(DIR_FEE)
    latest_contract = get_latest_file(DIR_CONTRACT)
    
    if not latest_fee or not latest_contract:
        print("❌ [오류] 소스 파일이 부족합니다.")
        return

    try:
        backup_master_file()
        df_master = pd.read_excel(FILE_MASTER, sheet_name=SHEET_NAME)
        df_fee = pd.read_excel(latest_fee)
        df_contract = pd.read_excel(latest_contract)

        # 1. 컬럼 매칭 (마스터는 '증권번호' 고정, 계약파일은 14번 인덱스)
        col_id_master = '증권번호'
        col_id_fee = '증권번호' # 수수료 파일은 '증권번호'로 잘 나옴
        col_id_contract = get_contract_id_column(df_contract)
        
        print(f"🔍 [ID 컬럼] 마스터: {col_id_master}, 수수료: {col_id_fee}, 계약: {col_id_contract}")

        # ID 문자열 정규화
        df_master[col_id_master] = df_master[col_id_master].astype(str).str.strip()
        df_fee[col_id_fee] = df_fee[col_id_fee].astype(str).str.strip()
        df_contract[col_id_contract] = df_contract[col_id_contract].astype(str).str.strip()

        # ---------------------------------------------------------
        # 2. 수수료 데이터 병합 (동일함)
        # ---------------------------------------------------------
        df_fee_sync = df_fee.rename(columns={col_id_fee: col_id_master})
        df_master.set_index(col_id_master, inplace=True)
        df_fee_sync.set_index(col_id_master, inplace=True)
        
        df_master.update(df_fee_sync)
        new_indices = df_fee_sync.index.difference(df_master.index)
        if not new_indices.empty:
            df_master = pd.concat([df_master, df_fee_sync.loc[new_indices]], axis=0)
        
        df_master.reset_index(inplace=True)

        # ---------------------------------------------------------
        # 3. 계약관리 데이터에서 '납입기간' 업데이트 (인덱스 기반 수정)
        # ---------------------------------------------------------
        # 계약파일: 납입기간(30번), 납입기간단위(31번)
        col_pay_val = df_contract.columns[30] if df_contract.shape[1] > 30 else None
        col_pay_unit = df_contract.columns[31] if df_contract.shape[1] > 31 else None
        
        # 마스터파일: '납입기간' 컬럼 찾기
        master_pay_col = '납입기간'
        
        if col_pay_val and col_pay_unit:
            print(f"🔄 [단계2] 납입기간 매핑 중... (계약컬럼: {col_pay_val})")
            
            # 매핑용 딕셔너리 (증권번호 -> 납입기간+단위)
            # 예: 30 + "년" -> "30년"
            def format_period(row):
                val = str(row[col_pay_val]).replace('.0', '')
                unit = str(row[col_pay_unit])
                if val == 'nan' or val == 'None': return None
                return f"{val}{unit}" if unit != 'nan' else val

            contract_map = df_contract.copy()
            contract_map['formatted_pay'] = contract_map.apply(format_period, axis=1)
            mapping_dict = contract_map.drop_duplicates(subset=[col_id_contract]).set_index(col_id_contract)['formatted_pay']
            
            df_master.set_index(col_id_master, inplace=True)
            common_idx = df_master.index.intersection(mapping_dict.index)
            
            # 실제 데이터 업데이트
            updated_count = 0
            for idx in common_idx:
                new_val = mapping_dict.loc[idx]
                if new_val:
                    df_master.loc[idx, master_pay_col] = new_val
                    updated_count += 1
            
            print(f"   ✅ {updated_count}건의 납입기간 정보 업데이트 완료.")
            df_master.reset_index(inplace=True)

        # ---------------------------------------------------------
        # 4. 저장
        # ---------------------------------------------------------
        all_sheets = pd.read_excel(FILE_MASTER, sheet_name=None)
        all_sheets[SHEET_NAME] = df_master

        with pd.ExcelWriter(FILE_MASTER, engine='openpyxl') as writer:
            for sheet_name, df_sheet in all_sheets.items():
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"\n🎉 [성공] 마스터 파일 업데이트 완료!")

    except Exception as e:
        print(f"❌ [에러] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_master()
