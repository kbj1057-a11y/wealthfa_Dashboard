"""
생명보험사 컬럼 구조 정밀 검증
- A~Y (1~25번 컬럼)이 정말 같은지 확인
- 25번: 환산성적 / TP 위치 확인
- 전체 컬럼 매핑 출력
"""
import os, warnings
warnings.filterwarnings("ignore")
import openpyxl

SOURCE_DIR = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료"

life_files = [
    ("(사업부)수입수수료산출_농협생명_202602.xlsx",    "농협생명"),
    ("(사업부)수입수수료산출_미래에셋생명_202602.xlsx", "미래에셋생명"),
    ("(사업부)수입수수료산출_삼성생명_202602.xlsx",    "삼성생명"),
]

# 엑셀 열 이름 (A=1, B=2 ... Z=26, AA=27)
def col_letter(n):
    letters = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters

print("=" * 70)
print("【생명보험사 전체 컬럼 매핑】")
print("=" * 70)

all_headers = {}

for filename, company in life_files:
    filepath = os.path.join(SOURCE_DIR, filename)
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    headers = []
    for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
        headers = [h for h in row]
        break
    wb.close()
    all_headers[company] = headers

    print(f"\n[{company}] 총 {len(headers)}개 컬럼")
    for i, h in enumerate(headers, 1):
        marker = ""
        if i == 25:
            marker = "  ← ★ 25번째(Y열)"
        if i <= 24:
            zone = "공통구간"
        elif h == "수수료계":
            zone = "수수료계"
        else:
            zone = "수수료항목"
        print(f"  {col_letter(i):>3} ({i:02d}): {str(h):<30s}  [{zone}]{marker}")

print("\n\n" + "=" * 70)
print("【A~Y (1~25번) 컬럼 3사 비교】")
print("=" * 70)

companies = [c for _, c in life_files]
max_col = max(len(h) for h in all_headers.values())

print(f"\n{'열':>4}  {'농협생명':<30}  {'미래에셋생명':<30}  {'삼성생명':<30}  일치여부")
print("-" * 115)

for i in range(1, 26):  # A(1) ~ Y(25)
    vals = []
    for company in companies:
        h = all_headers[company]
        vals.append(h[i-1] if i <= len(h) else None)

    # 일치 여부 체크 (None 제외)
    non_none = [v for v in vals if v is not None]
    if len(set(non_none)) <= 1:
        match = "✓ 일치"
    else:
        match = "✗ 불일치"

    letter = col_letter(i)
    print(f"  {letter}({i:02d})  {str(vals[0]):<30}  {str(vals[1]):<30}  {str(vals[2]):<30}  {match}")

print("\n\n" + "=" * 70)
print("【결론 요약】")
print("=" * 70)

# 1~24 공통 체크
print("\n[1~24번 컬럼] 공통 여부:")
for i in range(1, 25):
    vals = [all_headers[c][i-1] if i <= len(all_headers[c]) else None for c in companies]
    non_none = [v for v in vals if v is not None]
    match = "✓" if len(set(non_none)) <= 1 else "✗"
    print(f"  {col_letter(i):>3}({i:02d}): {str(vals[0]):<25} {match}")

# 25번 컬럼 (Y열) 체크
print(f"\n[25번 컬럼(Y열)] 환산성적/TP 확인:")
for company in companies:
    h = all_headers[company]
    val = h[24] if len(h) > 24 else "없음"
    print(f"  {company}: '{val}'")

# 마지막 컬럼 체크
print(f"\n[마지막 컬럼] 수수료계 위치:")
for company in companies:
    h = all_headers[company]
    last_val = h[-1]
    last_col = len(h)
    print(f"  {company}: {col_letter(last_col)}({last_col}번) = '{last_val}'")

print("\n\n>> 제안 구조 검토:")
print("   [공통 24개] + [환산 1개(Y열 통합)] + [수수료계 1개] = 총 26개 컬럼")
print("   ※ 단, 중간 수수료 세부항목(모집수수료, 계약관리 등)은 제외됨")
print("   ※ 생명보험사 3사 각각의 수수료 세부항목 개수:")
for company in companies:
    h = all_headers[company]
    fee_detail = [x for x in h[25:] if x and x != "수수료계"]
    print(f"      - {company}: {len(fee_detail)}개 수수료 세부항목 제외됨")
