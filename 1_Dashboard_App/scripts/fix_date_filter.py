path = r'G:\내 드라이브\안티그래비티\TEST\temp_push\app.py'
with open(path, 'r', encoding='utf-8') as f:
    t = f.read()

# 날짜 포맷 수정: '202601' -> '2026-01' (strftime('%Y-%m-%d') 결과에 맞게)
t = t.replace("str.startswith('202601', na=False)", "str.startswith('2026-01', na=False)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(t)

# 확인
count = t.count("startswith('2026-01'")
print(f"수정 완료: '2026-01' 패턴 {count}개 적용됨")
