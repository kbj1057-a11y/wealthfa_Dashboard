path = r'G:\내 드라이브\안티그래비티\TEST\temp_push\app.py'
with open(path, 'r', encoding='utf-8') as f:
    t = f.read()

# 1. @st.cache_data에 버전 키 추가 -> 캐시 강제 무효화
t = t.replace('@st.cache_data\ndef load_data():', '@st.cache_data(ttl=0)\ndef load_data():')

# 2. 계약일자_정제 컬럼이 있더라도 계약일자 원본(int)을 문자열로도 추가 보존
# find where we build the display col rename for detail table and add 계약일자 raw
# Also fix: strip whitespace from 계약일자 column usage

with open(path, 'w', encoding='utf-8') as f:
    f.write(t)

print("cache busted:", '@st.cache_data(ttl=0)' in t)
print("zfill fix present:", 'zfill(8)' in t)
print("format fix present:", "format='%Y%m%d'" in t)
