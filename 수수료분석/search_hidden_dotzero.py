import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"
SEARCH_KEY = "16505862"

print("============================================================")
print(f"증권번호 '{SEARCH_KEY}' 부분 문자열 검색 심층 진단 (.0 포함)")
print("============================================================")

xls2 = pd.ExcelFile(FILE2)

# 분석할 대상 시트 지정
sheets_to_check = ['생명보험']
manage_sheets = [s for s in xls2.sheet_names if '관리수수료' in s]
if manage_sheets:
    sheets_to_check.append(manage_sheets[0])

for sheet in sheets_to_check:
    print(f"\n[{sheet} 시트 검색 시작]")
    df = pd.read_excel(FILE2, sheet_name=sheet)
    
    if '증권번호' not in df.columns:
        print(f"  - '증권번호' 컬럼 없음")
        continue

    # 1. 엑셀에 들어있는 원본 형태(타입) 확인을 위해 우선 로우 데이터 추출
    # 2. 문자열 변환 후 검색
    # .astype(str) 시 float형은 1234.0 으로 변환됨
    df['원본타입'] = df['증권번호'].apply(type).astype(str)
    df['증권번호_str'] = df['증권번호'].astype(str)
    
    match = df[df['증권번호_str'].str.contains(SEARCH_KEY, na=False)]
    
    print(f"  > '{SEARCH_KEY}' 포함 데이터: {len(match)}건 발견")
    
    if not match.empty:
        fee_col = '수수료계' if sheet == '생명보험' else ('지사수수료' if '지사수수료' in df.columns else df.columns[-1])
        # 결과 출력
        res = match[['증권번호_str', '원본타입', fee_col]].copy()
        res.rename(columns={'증권번호_str': '엑셀내부_실제값'}, inplace=True)
        print(res.to_string(index=False))
