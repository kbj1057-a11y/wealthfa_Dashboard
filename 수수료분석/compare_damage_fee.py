import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*60)
print("손해보험사 증권번호 개수 및 일치 여부 분석")
print("="*60)

# ==========================================
# 1. 파일 1 (생손보통합) 처리 - 손해보험사 시트
# ==========================================
print(f"\n[1] 파일 로드 중: {FILE1.split(chr(92))[-1]}")
df1_damage = pd.read_excel(FILE1, sheet_name='손해보험사_202602', dtype=str)
if '증권번호' in df1_damage.columns:
    file1_ids = set(df1_damage['증권번호'].dropna().str.strip())
    print(f"  - 손해보험사 시트 총 행 수: {len(df1_damage):,}")
    print(f"  - 고유한 증권번호 수 (파일1): {len(file1_ids):,}")
else:
    print("  - [오류] 증권번호 컬럼을 찾을 수 없습니다.")
    file1_ids = set()

# ==========================================
# 2. 파일 2 (지사장상세) 처리
# ==========================================
print(f"\n[2] 파일 로드 중: {FILE2.split(chr(92))[-1]}")
xls2 = pd.ExcelFile(FILE2)

# 손해보험 상품군에 해당하는 시트들 ('장기', '자동차', '일반')
damage_sheets = [s for s in xls2.sheet_names if s in ['장기', '자동차', '일반']]
file2_detail_ids = set()

for sheet in damage_sheets:
    df_temp = pd.read_excel(FILE2, sheet_name=sheet, dtype=str)
    if '증권번호' in df_temp.columns:
        ids = set(df_temp['증권번호'].dropna().str.strip())
        file2_detail_ids.update(ids)
        print(f"  - [{sheet}] 고유 증권번호 수: {len(ids):,}")

# 관리수수료 시트 중 "손해보험사" (생명보험이 아닌 것)
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage, dtype=str)

file2_manage_ids = set()
if '증권번호' in df2_manage.columns and '제휴사' in df2_manage.columns:
    # 제휴사명에 '생명'이 들어가지 않은 데이터를 손해보험사로 간주
    damage_manage_df = df2_manage[~df2_manage['제휴사'].astype(str).str.contains('생명', na=False)]
    file2_manage_ids = set(damage_manage_df['증권번호'].dropna().str.strip())
    print(f"  - [{sheet_manage} (손해보험만)] 고유 증권번호 수: {len(file2_manage_ids):,}")

# 파일2의 손해보험 관련 증권번호 총합 (상세 시트들 + 관리수수료 시트 손해분)
file2_total_ids = file2_detail_ids.union(file2_manage_ids)
print(f"  => 파일 2 (장기/자동차/일반 + 관리손보) 고유 증권번호 총합 수: {len(file2_total_ids):,}")

# ==========================================
# 3. 비교
# ==========================================
print("\n" + "="*60)
print("비교 결과")
print("="*60)
print(f"1번 파일(통합) 손해보험사 증권번호 수: {len(file1_ids):,}")
print(f"2번 파일(상세) 손해보험사 증권번호 수: {len(file2_total_ids):,}")

diff_1_not_2 = file1_ids - file2_total_ids
diff_2_not_1 = file2_total_ids - file1_ids

print(f"\n[일치 여부 확인]")
if file1_ids == file2_total_ids:
    print("✅ 두 파일의 손해보험사 증권번호가 완벽하게 일치합니다!")
else:
    print("❌ 불일치 발생!")
    print(f"  - 1번 파일에만 있는 증권번호 수: {len(diff_1_not_2):,}")
    print(f"  - 2번 파일에만 있는 증권번호 수: {len(diff_2_not_1):,}")
    
    # 누락된 데이터 몇 개만 샘플로 보여줌
    if len(diff_1_not_2) > 0:
        print(f"\n[샘플] 1번 파일에만 있는 증권번호 (최대 5개):")
        for i, val in enumerate(list(diff_1_not_2)[:5]):
            print(f"   {i+1}. {val}")
            
    if len(diff_2_not_1) > 0:
        print(f"\n[샘플] 2번 파일에만 있는 증권번호 (최대 5개):")
        for i, val in enumerate(list(diff_2_not_1)[:5]):
            print(f"   {i+1}. {val}")
