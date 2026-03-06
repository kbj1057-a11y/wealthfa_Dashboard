import re

path = r'G:\내 드라이브\안티그래비티\TEST\temp_push\app.py'
with open(path, 'r', encoding='utf-8') as f:
    t = f.read()

# 1. load_data 내의 잘못된 rename 코드 (escape된 것) 제거 후 올바른 코드로 교체
old_rename = (
    "    # 여기서 실제 컨럼명 → 코드 상의 변수명으로 rename (CSV 파일과 코드의 다리 'bridge')\n"
    "    df_life   = df_life.rename(columns={'\\ud658\\uc0b0\\uc131\\uc801': '\\uc5c5\\uc801\\uc9c01', '\\ubcf4\\ud5d8\\ub8cc': '\\uc5c5\\uc801\\uc9c02'})\n"
    "    df_damage = df_damage.rename(columns={'\\uc218\\uc815\\ubcf4\\ud5d8\\ub8cc': '\\uc5c5\\uc801\\uc9c03', '\\ubcf4\\ud5d8\\ub8cc': '\\uc5c5\\uc801\\uc9c02'})\n\n"
)

new_rename = (
    "    # 실제 컬럼명 → 코드 통일 변수명 bridge rename\n"
    "    df_life   = df_life.rename(columns={'환산성적': '업적지표1', '보험료': '업적지표2'})\n"
    "    df_damage = df_damage.rename(columns={'수정보험료': '업적지표3', '보험료': '업적지표2'})\n\n"
)
t = t.replace(old_rename, new_rename)

# 2. 잘못된 escape 날짜/numeric 코드도 교체
old_numeric = (
    "    # \\ub0a0\\uc9dc \\uc815\\uc81c\n"
    "    if '\\uacc4\\uc57d\\uc77c\\uc790' in df_all.columns:\n"
    "        df_all['\\uacc4\\uc57d\\uc77c\\uc790_\\uc815\\uc81c'] = pd.to_datetime(df_all['\\uacc4\\uc57d\\uc77c\\uc790'], errors='coerce').dt.strftime('%Y-%m-%d')\n"
    "    else:\n"
    "        df_all['\\uacc4\\uc57d\\uc77c\\uc790_\\uc815\\uc81c'] = ''\n\n"
    "    # \\uc218\\uce58\\ud615 \\ucf58\\ub7fc \\ucc98\\ub9ac (\\uc2e4\\uc81c \\ucee8\\ub7fc\\uba85 + rename \\ud6c4 \\ucee8\\ub7fc\\uba85 \\ubaa8\\ub450 \\ud3ec\\ud568)\n"
    "    numeric_cols = ['\\uc9c0\\uc0ac\\uc218\\uc218\\ub8cc', '\\uc5c5\\uc801\\uc9c01', '\\uc5c5\\uc801\\uc9c02', '\\uc5c5\\uc801\\uc9c03',\n"
    "                    '\\ud658\\uc0b0\\uc131\\uc801', '\\ubcf4\\ud5d8\\ub8cc', '\\uc218\\uc815\\ubcf4\\ud5d8\\ub8cc', 'FC\\uc218\\uc218\\ub8cc']\n"
)
new_numeric = (
    "    # 날짜 정제\n"
    "    if '계약일자' in df_all.columns:\n"
    "        df_all['계약일자_정제'] = pd.to_datetime(df_all['계약일자'], errors='coerce').dt.strftime('%Y-%m-%d')\n"
    "    else:\n"
    "        df_all['계약일자_정제'] = ''\n\n"
    "    # 수치형 컬럼 처리\n"
    "    numeric_cols = ['지사수수료', '업적지표1', '업적지표2', '업적지표3', 'FC수수료', '보험료', '환산성적']\n"
)
t = t.replace(old_numeric, new_numeric)

with open(path, 'w', encoding='utf-8') as f:
    f.write(t)

print("Done. Checking key strings:")
print("- '환산성적' in file:", '환산성적' in t)
print("- '업적지표1' rename in file:", "rename(columns={'환산성적': '업적지표1'" in t)
