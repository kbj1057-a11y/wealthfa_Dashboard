import codecs

path = r'G:\내 드라이브\안티그래비티\TEST\dashboard_app.py'
t = codecs.open(path, 'r', 'utf-8').read()

# 1. HTML class 교체: unit-text -> unit-won
t = t.replace("class='unit-text'", "class='unit-won'")
t = t.replace('class="unit-text"', 'class="unit-won"')

# 2. CSS 클래스명 교체
t = t.replace('.unit-text {', '.unit-won {')
t = t.replace('.unit-text{', '.unit-won{')

# 3. CSS에 남아있을 수 있는 inline style= 중 unit-text 참조까지 정리
count = t.count('unit-won')
codecs.open(path, 'w', 'utf-8').write(t)
print(f"Done. unit-won count: {count}")
