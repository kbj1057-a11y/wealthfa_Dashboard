
import pandas as pd
import glob
import os
import sys

# 한글 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# 경로 설정
FEE_DIR = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
TARGET_FILE = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년업적,수수료통계.xlsx"

def inspect_columns():
    try:
        # 1. 최신 수수료 파일 찾기
        fee_files = glob.glob(os.path.join(FEE_DIR, "*.xlsx"))
        fee_files = [f for f in fee_files if not os.path.basename(f).startswith("~$")]
        if not fee_files:
            print(f"❌ '{FEE_DIR}' 폴더에 엑셀 파일이 없습니다.")
            return

        latest_fee_file = max(fee_files, key=os.path.getctime)
        print(f"📂 [소스] 최신 수수료 파일: {os.path.basename(latest_fee_file)}")
        
        df_fee = pd.read_excel(latest_fee_file)
        fee_cols = df_fee.columns.tolist()
        print(f"   - 컬럼 수: {len(fee_cols)}")
        print(f"   - 컬럼 목록: {fee_cols}")
        print("-" * 50)

        # 2. 타겟 마스터 파일 읽기
        if not os.path.exists(TARGET_FILE):
            print(f"❌ [타겟] 파일이 존재하지 않습니다: {TARGET_FILE}")
            return

        print(f"📂 [타겟] 마스터 파일: {os.path.basename(TARGET_FILE)}")
        df_target = pd.read_excel(TARGET_FILE)
        target_cols = df_target.columns.tolist()
        print(f"   - 컬럼 수: {len(target_cols)}")
        print(f"   - 컬럼 목록: {target_cols}")
        print("-" * 50)
        
        # 3. 컬럼 비교 (간단)
        common_cols = set(fee_cols) & set(target_cols)
        only_in_target = set(target_cols) - set(fee_cols)
        only_in_fee = set(fee_cols) - set(target_cols)
        
        print(f"✅ 공통 컬럼: {len(common_cols)}개")
        if only_in_target:
            print(f"⚠️ 타겟에만 있는 컬럼 (유지됨): {only_in_target}")
        if only_in_fee:
            print(f"🆕 소스에만 있는 컬럼 (추가될 수 있음): {only_in_fee}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    inspect_columns()
