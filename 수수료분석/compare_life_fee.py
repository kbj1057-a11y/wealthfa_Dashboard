import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"

print("="*60)
print("증권번호 개수 및 일치 여부 분석")
print("="*60)

# ==========================================
# 1. 파일 1 (생손보통합) 처리
# ==========================================
print(f"\n[1] 파일 로드 중: {FILE1.split(chr(92))[-1]}")
df1_life = pd.read_excel(FILE1, sheet_name='생명보험사_202602', dtype=str)
# 컬럼에 '증권번호'가 있는지 확인
if '증권번호' in df1_life.columns:
    file1_ids = set(df1_life['증권번호'].dropna().str.strip())
    print(f"  - 생명보험사 시트 행 수: {len(df1_life):,}")
    print(f"  - 고유한 증권번호 수: {len(file1_ids):,}")
else:
    print("  - [오류] 증권번호 컬럼을 찾을 수 없습니다.")
    file1_ids = set()

# ==========================================
# 2. 파일 2 (지사장상세) 처리
# ==========================================
print(f"\n[2] 파일 로드 중: {FILE2.split(chr(92))[-1]}")
xls2 = pd.ExcelFile(FILE2)
print(f"  - 시트 목록: {xls2.sheet_names}")

# 2-1) 생명보험사 시트 (이름 유추: '생명보험' 형태일 수 있음)
sheet_life = [s for s in xls2.sheet_names if '생명' in s][0]
df2_life = pd.read_excel(FILE2, sheet_name=sheet_life, dtype=str)

# 2-2) 관리수수료 시트
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s][0]
df2_manage = pd.read_excel(FILE2, sheet_name=sheet_manage, dtype=str)

# 컬럼 파악
print(f"\n[시트: {sheet_life}] 컬럼: {df2_life.columns.tolist()[:10]}")
print(f"[시트: {sheet_manage}] 컬럼: {df2_manage.columns.tolist()[:10]}")

file2_life_ids = set()
if '증권번호' in df2_life.columns:
    file2_life_ids = set(df2_life['증권번호'].dropna().str.strip())
    print(f"  - [{sheet_life}] 고유 증권번호 수: {len(file2_life_ids):,}")

file2_manage_ids = set()
if '증권번호' in df2_manage.columns and '보험사' in df2_manage.columns: # 제휴사 또는 보험사
    # 생명보험사만 필터 (보통 '생명'이라는 단어가 보험사명에 포함됨)
    life_manage_df = df2_manage[df2_manage['보험사'].astype(str).str.contains('생명', na=False)]
    file2_manage_ids = set(life_manage_df['증권번호'].dropna().str.strip())
    print(f"  - [{sheet_manage} (생명만)] 고유 증권번호 수: {len(file2_manage_ids):,}")
elif '증권번호' in df2_manage.columns and '제휴사' in df2_manage.columns:
    life_manage_df = df2_manage[df2_manage['제휴사'].astype(str).str.contains('생명', na=False)]
    file2_manage_ids = set(life_manage_df['증권번호'].dropna().str.strip())
    print(f"  - [{sheet_manage} (생명만)] 고유 증권번호 수: {len(file2_manage_ids):,}")
else:
    print("  - [오류] 관리수수료 시트에서 '증권번호'나 '보험사(제휴사)' 컬럼을 찾을 수 없습니다.")

# 합집합
file2_total_ids = file2_life_ids.union(file2_manage_ids)
print(f"  => 파일 2 (생명+관리생명) 고유 증권번호 총합 수: {len(file2_total_ids):,}")

# ==========================================
# 3. 비교
# ==========================================
print("\n" + "="*60)
print("비교 결과")
print("="*60)
print(f"1번 파일(통합) 증권번호 수: {len(file1_ids):,}")
print(f"2번 파일(상세) 증권번호 수: {len(file2_total_ids):,}")

diff_1_not_2 = file1_ids - file2_total_ids
diff_2_not_1 = file2_total_ids - file1_ids

print(f"\n[일치 여부 확인]")
if file1_ids == file2_total_ids:
    print("✅ 두 파일의 증권번호가 완벽하게 일치합니다!")
else:
    print("❌ 불일치 발생!")
    print(f"  - 1번 파일에만 있는 증권번호 수: {len(diff_1_not_2):,}")
    print(f"  - 2번 파일에만 있는 증권번호 수: {len(diff_2_not_1):,}")

print("\n(분석 완료)")
