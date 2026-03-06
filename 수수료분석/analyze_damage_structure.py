"""
손해보험사 컬럼 구조 정밀 분석
- A~X (1~24번) 공통 구간 확인
- 25번 이후 수수료 시작점 분석
- 수수료 컬럼 그룹 비교
- 결과를 txt 파일로 저장
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl

SOURCE_DIR = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료"
OUTPUT_FILE = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\damage_structure_analysis.txt"

damage_files = [
    ("(사업부)수입수수료산출_AIG손해보험_202602.xlsx",  "AIG손해보험"),
    ("(사업부)수입수수료산출_DB손해보험_202602.xlsx",   "DB손해보험"),
    ("(사업부)수입수수료산출_KB손해보험_202602.xlsx",   "KB손해보험"),
    ("(사업부)수입수수료산출_롯데손해보험_202602.xlsx",  "롯데손해보험"),
    ("(사업부)수입수수료산출_메리츠화재_202602.xlsx",   "메리츠화재"),
    ("(사업부)수입수수료산출_삼성화재_202602.xlsx",    "삼성화재"),
    ("(사업부)수입수수료산출_하나손해_202602.xlsx",    "하나손해"),
    ("(사업부)수입수수료산출_한화손해보험_202602.xlsx",  "한화손해보험"),
    ("(사업부)수입수수료산출_현대해상_202602.xlsx",    "현대해상"),
    ("(사업부)수입수수료산출_흥국화재_202602.xlsx",    "흥국화재"),
]

def col_letter(n):
    letters = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        letters = chr(65 + r) + letters
    return letters

# 헤더 로딩
all_headers = {}
for filename, company in damage_files:
    filepath = os.path.join(SOURCE_DIR, filename)
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
        all_headers[company] = [h for h in row]
        break
    wb.close()

lines = []
companies = [c for _, c in damage_files]

# ─────────────────────────────────────────────────────
# 1. 회사별 전체 컬럼 목록
# ─────────────────────────────────────────────────────
lines.append("=" * 80)
lines.append("【손해보험사 회사별 전체 컬럼 목록】")
lines.append("=" * 80)

for company in companies:
    headers = all_headers[company]
    lines.append(f"\n[{company}] 총 {len(headers)}개 컬럼")
    for i, h in enumerate(headers, 1):
        if i <= 24:
            zone = "공통구간"
        elif str(h) == "수수료계":
            zone = "수수료계"
        else:
            zone = "수수료항목"
        marker = "  ← ★ 25번(Y열)" if i == 25 else ""
        lines.append(f"  {col_letter(i):>3}({i:02d}): {str(h):<35} [{zone}]{marker}")

# ─────────────────────────────────────────────────────
# 2. 공통 컬럼 구간(1~24) 비교표
# ─────────────────────────────────────────────────────
lines.append("\n\n" + "=" * 80)
lines.append("【A~X (1~24번) 공통 구간 비교】")
lines.append("=" * 80)

header_line = f"{'열':>5}  {'컬럼명(기준:AIG)':^25}"
for company in companies:
    header_line += f"  {company[:6]:^10}"
header_line += "  일치여부"
lines.append(header_line)
lines.append("-" * 150)

for i in range(1, 25):
    vals = [all_headers[c][i-1] if i <= len(all_headers[c]) else None for c in companies]
    base = str(vals[0])
    non_none = [v for v in vals if v is not None]
    match = "OK" if len(set(non_none)) <= 1 else "!불일치!"
    row_str = f"  {col_letter(i)}({i:02d})  {base:<25}"
    for v in vals:
        match_mark = "     OK" if str(v) == base else f"  {str(v)[:8]}"
        row_str += match_mark
    row_str += f"  {match}"
    lines.append(row_str)

# ─────────────────────────────────────────────────────
# 3. 25번째 컬럼 (Y열) - 첫 번째 수수료 항목 비교
# ─────────────────────────────────────────────────────
lines.append("\n\n" + "=" * 80)
lines.append("【25번째 컬럼(Y열) - 수수료 시작 컬럼 비교】")
lines.append("=" * 80)

col25_vals = {}
for company in companies:
    h = all_headers[company]
    v = h[24] if len(h) > 24 else "없음"
    col25_vals[company] = v

for company, v in col25_vals.items():
    lines.append(f"  {company:<15}: '{v}'")

# 25번 고유값 분석
unique_col25 = set(col25_vals.values())
lines.append(f"\n  >> 25번 컬럼 고유 값: {sorted(unique_cols := unique_col25)}")
if len(unique_col25) == 1:
    lines.append(f"  >> 10개사 모두 동일: '{list(unique_col25)[0]}'")
else:
    lines.append(f"  >> {len(unique_col25)}가지 다른 값 존재 → 통일 필요 여부 검토")
    for uv in sorted(unique_col25):
        same = [c for c, v in col25_vals.items() if v == uv]
        lines.append(f"     '{uv}': {same}")

# ─────────────────────────────────────────────────────
# 4. 수수료 항목 컬럼 분석 (25번~, 수수료계 제외)
# ─────────────────────────────────────────────────────
lines.append("\n\n" + "=" * 80)
lines.append("【수수료 세부항목 컬럼 분석 (25번 이후)】")
lines.append("=" * 80)

fee_by_company = {}
for company in companies:
    h = all_headers[company]
    fee_cols = [str(x) for x in h[24:] if x is not None and str(x) != "수수료계"]
    fee_by_company[company] = fee_cols
    lines.append(f"\n  [{company}] 수수료 세부항목 {len(fee_cols)}개:")
    for i, c in enumerate(fee_cols, 1):
        lines.append(f"    {i:02d}. {c}")

# 교집합 (모든 회사 공통)
sets = [set(v) for v in fee_by_company.values()]
common_all = sets[0].copy()
for s in sets[1:]:
    common_all &= s
union_all = set().union(*sets)

lines.append(f"\n  >> 10개사 공통 수수료 컬럼 ({len(common_all)}개):")
for c in sorted(common_all):
    lines.append(f"     - {c}")

# 과반수(5개사 이상) 공통
lines.append(f"\n  >> 5개사 이상 보유한 수수료 컬럼 (주요 항목):")
for col in sorted(union_all):
    count = sum(1 for s in sets if col in s)
    if count >= 5:
        companies_with = [c for c, v in fee_by_company.items() if col in v]
        lines.append(f"     - {col:<30} ({count}개사): {', '.join(companies_with)}")

# 전체 고유 컬럼 수
lines.append(f"\n  >> 손해보험사 전체 고유 수수료 컬럼: {len(union_all)}개")

# ─────────────────────────────────────────────────────
# 5. 최종 구조 요약 (안 B 기준)
# ─────────────────────────────────────────────────────
lines.append("\n\n" + "=" * 80)
lines.append("【최종 구조 요약 (안 B: 구조 유지)】")
lines.append("=" * 80)

# 전체 unique 수수료 컬럼 (순서 보존)
fee_ordered = []
fee_seen = set()
for company in companies:
    for c in fee_by_company[company]:
        if c not in fee_seen:
            fee_ordered.append(c)
            fee_seen.add(c)

total_cols = 24 + len(fee_ordered) + 1  # 공통 + 수수료세부 + 수수료계
lines.append(f"\n  공통 컬럼        : 24개  (A~X: 번호~보험료)")
lines.append(f"  25번 컬럼(Y열)   : 회사별 첫 수수료 항목 (이름 다양)")
lines.append(f"  수수료 세부항목  : {len(fee_ordered)}개  (각 회사 고유 항목 합산)")
lines.append(f"  수수료계         : 1개   (맨 마지막)")
lines.append(f"  ────────────────────────────")
lines.append(f"  손해보험사 시트 총 컬럼: {total_cols}개")
lines.append(f"\n  [수수료 세부항목 전체 목록 {len(fee_ordered)}개]")
for i, c in enumerate(fee_ordered, 1):
    lines.append(f"    {i:02d}. {c}")

# 저장
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"분석 완료: {OUTPUT_FILE}", file=sys.stderr)
