"""
생명보험사 vs 손해보험사 컬럼 구조 비교 분석
- 파일명에 '생명' 포함 → 생명보험사
- 그 외 → 손해보험사
"""
import os
import warnings
warnings.filterwarnings("ignore")
import openpyxl

SOURCE_DIR = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료"

excel_files = sorted([
    f for f in os.listdir(SOURCE_DIR)
    if f.endswith(".xlsx") and not f.startswith("~$")
])

# ─────────────────────────────────────────
# 회사 분류
# ─────────────────────────────────────────
life_files   = []  # 생명보험사
damage_files = []  # 손해보험사

for f in excel_files:
    company = f.replace("(사업부)수입수수료산출_", "").replace("_202602.xlsx", "")
    if "생명" in company:
        life_files.append((f, company))
    else:
        damage_files.append((f, company))

out_lines = []
out_lines.append("=" * 80)
out_lines.append("【생명보험사 분류】")
out_lines.append("=" * 80)
for f, c in life_files:
    out_lines.append(f"  - {c}")

out_lines.append("")
out_lines.append("=" * 80)
out_lines.append("【손해보험사 분류】")
out_lines.append("=" * 80)
for f, c in damage_files:
    out_lines.append(f"  - {c}")

COMMON_COL_COUNT = 24  # 번호~보험료

def get_fee_columns(filename):
    filepath = os.path.join(SOURCE_DIR, filename)
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    headers = []
    for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
        headers = [str(h) if h is not None else None for h in row]
        break
    wb.close()
    # 24번 이후 수수료 컬럼 (수수료계 제외)
    fee_cols = [h for h in headers[COMMON_COL_COUNT:] if h and h != "수수료계"]
    return fee_cols, headers[:COMMON_COL_COUNT]

# ─────────────────────────────────────────
# 생명보험사 분석
# ─────────────────────────────────────────
out_lines.append("")
out_lines.append("=" * 80)
out_lines.append("【생명보험사 - 수수료 컬럼 상세】")
out_lines.append("=" * 80)

life_all_fee_cols = set()
life_fee_by_company = {}

for filename, company in life_files:
    fee_cols, common = get_fee_columns(filename)
    life_fee_by_company[company] = fee_cols
    life_all_fee_cols.update(fee_cols)
    out_lines.append(f"\n  [{company}] - {len(fee_cols)}개 수수료 컬럼")
    for i, c in enumerate(fee_cols, 1):
        out_lines.append(f"    {i:02d}. {c}")

# 생명보험사 공통 컬럼
if life_fee_by_company:
    sets = [set(v) for v in life_fee_by_company.values()]
    life_common = sets[0]
    for s in sets[1:]:
        life_common &= s
    life_union  = set().union(*sets)

    out_lines.append(f"\n  >> 생명보험사 그룹 공통 수수료 컬럼 ({len(life_common)}개):")
    for c in sorted(life_common):
        out_lines.append(f"       - {c}")
    out_lines.append(f"\n  >> 생명보험사 전체 고유 수수료 컬럼 ({len(life_union)}개):")
    for c in sorted(life_union):
        out_lines.append(f"       - {c}")

# ─────────────────────────────────────────
# 손해보험사 분석
# ─────────────────────────────────────────
out_lines.append("")
out_lines.append("=" * 80)
out_lines.append("【손해보험사 - 수수료 컬럼 상세】")
out_lines.append("=" * 80)

damage_all_fee_cols = set()
damage_fee_by_company = {}

for filename, company in damage_files:
    fee_cols, common = get_fee_columns(filename)
    damage_fee_by_company[company] = fee_cols
    damage_all_fee_cols.update(fee_cols)
    out_lines.append(f"\n  [{company}] - {len(fee_cols)}개 수수료 컬럼")
    for i, c in enumerate(fee_cols, 1):
        out_lines.append(f"    {i:02d}. {c}")

if damage_fee_by_company:
    sets = [set(v) for v in damage_fee_by_company.values()]
    damage_common = sets[0]
    for s in sets[1:]:
        damage_common &= s
    damage_union = set().union(*sets)

    out_lines.append(f"\n  >> 손해보험사 그룹 공통 수수료 컬럼 ({len(damage_common)}개):")
    for c in sorted(damage_common):
        out_lines.append(f"       - {c}")
    out_lines.append(f"\n  >> 손해보험사 전체 고유 수수료 컬럼 ({len(damage_union)}개):")
    for c in sorted(damage_union):
        out_lines.append(f"       - {c}")

# ─────────────────────────────────────────
# 생명 vs 손해 교차 분석
# ─────────────────────────────────────────
out_lines.append("")
out_lines.append("=" * 80)
out_lines.append("【생명 vs 손해 - 교차 분석】")
out_lines.append("=" * 80)

life_u   = set().union(*[set(v) for v in life_fee_by_company.values()]) if life_fee_by_company else set()
damage_u = set().union(*[set(v) for v in damage_fee_by_company.values()]) if damage_fee_by_company else set()

both_groups = life_u & damage_u
only_life   = life_u - damage_u
only_damage = damage_u - life_u

out_lines.append(f"\n  >> 양쪽 모두 존재하는 컬럼 ({len(both_groups)}개):")
for c in sorted(both_groups):
    out_lines.append(f"       - {c}")
out_lines.append(f"\n  >> 생명보험사에만 있는 컬럼 ({len(only_life)}개):")
for c in sorted(only_life):
    out_lines.append(f"       - {c}")
out_lines.append(f"\n  >> 손해보험사에만 있는 컬럼 ({len(only_damage)}개):")
for c in sorted(only_damage):
    out_lines.append(f"       - {c}")

# 파일로 저장
result_path = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\column_analysis_life_vs_damage.txt"
with open(result_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print(f"분석 완료: {result_path}", flush=True)
