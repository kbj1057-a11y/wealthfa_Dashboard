import pandas as pd
import glob
import os
import shutil
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

DIR_FEE = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
FILE_MASTER = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"
SHEET_NAME = "RAWDATA"

# 계약 파일 컬럼 인덱스 (실제 데이터 기반 확인)
CONTRACT_ID_COL_IDX = 14   # 증권번호에 해당 (y컬럼)
CONTRACT_DATE_COL = '계약일자'  # 28번 인덱스
CONTRACT_COLS_MAP = {
    # 계약 파일 컬럼명 -> 마스터 파일 컬럼명
    '제휴사': '제휴사',
    'FC코드': 'FC코드',
    'FC명': 'FC명',
    '계약종류': '계약종류',
    '상품종류': '상품종류',
    '상품명': '상품명',
    '상품명비고': '상품명비고',
    '보험료': '보험료',
    '보험사환산_1차년': '보험사환산_1차년',
    '보험사환산_2차년': '보험사환산_2차년',
    '보험사환산_3차년': '보험사환산_3차년',
    '조정환산(STP)': '조정환산(STP)',
    '조정환산(STP)_1차년': '조정환산(STP)_1차년',
    '조정환산(STP)_2차년': '조정환산(STP)_2차년',
    '조정환산(STP)_3차년': '조정환산(STP)_3차년',
    '계약상태': '계약상태',
    '계약일자': '계약일자',
    '최종납월': '최종납월',
    '납입기간': '납입기간',
    '납입기간명': '납입기간명',
    '시작일자': '시작일자',
    '종료일자': '종료일자',
    '납입주기(방법)': '납입주기(방법)',
    '수금방법': '수금방법',
    '계약자': '계약자',
    '피보험자': '피보험자',
    '지역': '지역',
    '기타': '기타',
    '본인·가족계약': '본인·가족계약',
    '개인정보동의서': '개인정보동의서',
    '상품비교설명서': '상품비교설명서',
    '외부이관여부': '외부이관여부',
    '비고': '비고',
    '지사': '지사',
    '본부': '본부',
    '맵핑상태': '맵핑상태',
    '영업단': '영업단',
    '지점': '지점',
    '팀': '팀',
    '해피콜': '해피콜',
    '해피콜등록일자': '해피콜등록일자',
}

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
    print(f"📦 [백업] 완료: {os.path.basename(backup_path)}")

def update_master():
    print("======== 마스터 파일 업데이트 (계약 신규 추가 수정버전) ========")

    latest_fee = get_latest_file(DIR_FEE)
    latest_contract = get_latest_file(DIR_CONTRACT)

    if not latest_fee or not latest_contract:
        print("❌ 소스 파일이 없습니다.")
        return

    print(f"📂 수수료: {os.path.basename(latest_fee)}")
    print(f"📂 계약:   {os.path.basename(latest_contract)}")

    try:
        backup_master_file()

        df_master = pd.read_excel(FILE_MASTER, sheet_name=SHEET_NAME)
        df_fee = pd.read_excel(latest_fee)
        df_contract = pd.read_excel(latest_contract)

        # 마스터 가입수 기록
        master_before = len(df_master)
        
        # ==============================================
        # [1단계] 수수료 파일 -> 마스터 업데이트
        # 수수료 파일의 ID: '증권번호' 컬럼 (동일)
        # ==============================================
        print("\n🔄 [1단계] 수수료 데이터 병합...")
        col_id = '증권번호'
        df_master[col_id] = df_master[col_id].astype(str).str.strip()
        df_fee[col_id] = df_fee[col_id].astype(str).str.strip()

        df_master.set_index(col_id, inplace=True)
        df_fee.set_index(col_id, inplace=True)
        df_master.update(df_fee)

        # 수수료 파일에만 있는 신규 항목 추가
        new_fee_ids = df_fee.index.difference(df_master.index)
        if not new_fee_ids.empty:
            print(f"   🆕 수수료발 신규 {len(new_fee_ids)}건 추가")
            df_master = pd.concat([df_master, df_fee.loc[new_fee_ids]], axis=0)

        df_master.reset_index(inplace=True)

        # ==============================================
        # [2단계] 계약 파일 -> 마스터에 신규 계약 추가
        # 계약 파일의 ID: df_contract.columns[14] ('y' 컬럼 = 실제 증권번호)
        # ==============================================
        print("\n🔄 [2단계] 계약 파일 신규 계약 추가...")
        col_id_contract = df_contract.columns[CONTRACT_ID_COL_IDX]
        df_contract[col_id_contract] = df_contract[col_id_contract].astype(str).str.strip()
        df_master[col_id] = df_master[col_id].astype(str).str.strip()

        master_ids = set(df_master[col_id])
        contract_ids = set(df_contract[col_id_contract])
        new_ids = contract_ids - master_ids

        if new_ids:
            print(f"   🆕 계약발 신규 {len(new_ids)}건 발견, 마스터에 추가 중...")
            new_rows = df_contract[df_contract[col_id_contract].isin(new_ids)].copy()
            
            # 계약 파일 컬럼 중 마스터와 대응되는 것 매핑
            # 계약파일의 'y'컬럼 -> 마스터의 '증권번호'로 이름 변경
            new_rows = new_rows.rename(columns={col_id_contract: col_id})
            
            # 마스터에 없는 필수 컬럼은 NaN으로 채워짐
            df_master = pd.concat([df_master, new_rows], axis=0, ignore_index=True)
            print(f"   ✅ 추가된 신규 계약:")
            for nid in new_ids:
                row = new_rows[new_rows[col_id] == nid].iloc[0]
                print(f"      - {nid} | FC: {row.get('FC명', '?')} | 제휴사: {row.get('제휴사', '?')} | 계약일: {row.get('계약일자', '?')}")
        else:
            print("   ℹ️ 신규 계약 없음.")

        # ==============================================
        # [3단계] 납입기간 업데이트
        # ==============================================
        print("\n🔄 [3단계] 납입기간 업데이트...")
        col_pay_val = df_contract.columns[30]  # 납입기간
        col_pay_unit = df_contract.columns[31]  # 납입기간명
        col_id_c = col_id  # 이미 rename 되어 있으므로 그냥 증권번호 사용

        def format_period(row):
            val = str(row[col_pay_val]).replace('.0', '')
            unit = str(row[col_pay_unit])
            if val in ('nan', 'None', ''): return None
            return f"{val}{unit}" if unit not in ('nan', 'None') else val

        df_contract_renamed = df_contract.rename(columns={df_contract.columns[CONTRACT_ID_COL_IDX]: col_id})
        df_contract_renamed['formatted_pay'] = df_contract_renamed.apply(format_period, axis=1)
        mapping_dict = df_contract_renamed.dropna(subset=['formatted_pay']).drop_duplicates(
            subset=[col_id]).set_index(col_id)['formatted_pay']

        df_master.set_index(col_id, inplace=True)
        common_idx = df_master.index.intersection(mapping_dict.index)
        df_master.loc[common_idx, '납입기간'] = mapping_dict.loc[common_idx]
        df_master.reset_index(inplace=True)
        print(f"   ✅ 납입기간 {len(common_idx)}건 업데이트 완료.")

        # ==============================================
        # [4단계] 저장
        # ==============================================
        print("\n💾 마스터 파일 저장 중...")
        all_sheets = pd.read_excel(FILE_MASTER, sheet_name=None)
        all_sheets[SHEET_NAME] = df_master

        with pd.ExcelWriter(FILE_MASTER, engine='openpyxl') as writer:
            for sn, ds in all_sheets.items():
                ds.to_excel(writer, sheet_name=sn, index=False)

        print(f"\n🎉 [성공] 마스터 파일 업데이트 완료!")
        print(f"   업데이트 전: {master_before}건 → 업데이트 후: {len(df_master)}건")

    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_master()
