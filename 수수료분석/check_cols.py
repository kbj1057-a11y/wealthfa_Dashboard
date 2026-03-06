import pandas as pd
import json

df1 = pd.read_excel(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx', sheet_name='생명보험사_202602')
df2 = pd.read_excel(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx', sheet_name='손해보험사_202602')

res = {
    '생명': [c for c in df1.columns if '지급' in c or '구분' in c],
    '손해': [c for c in df2.columns if '지급' in c or '구분' in c]
}
with open(r'G:\내 드라이브\안티그래비티\TEST\수수료분석\cols.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False)
