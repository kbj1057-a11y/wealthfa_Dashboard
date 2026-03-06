import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"
OUTPUT_FILE = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서.xlsx"

print("="*60)
print("1번, 2번 파일 병합 작업 시작 (A~X 유지 / Y, Z, AA 추가)")
print("="*60)

# ==========================================
# 1. 파일 2 (상세내역) 데이터사전 만들기
# ==========================================
print("[1] 2번 파일(상세내역) 로드 및 증권번호별 데이터 딕셔너리 생성 중...")
xls2 = pd.ExcelFile(FILE2)

def get_sum_dict(df, id_col, val_col):
    if id_col in df.columns and val_col in df.columns:
        df[val_col] = pd.to_numeric(df[val_col], errors='coerce').fillna(0)
        return df.groupby(id_col)[val_col].sum().to_dict()
    return {}

dict_fc_fee = {}
dict_raw_fee = {}
dict_manage_fee = {}
dict_bundam = {}

# (1) 생명보험, 장기, 자동차, 일반 (원 수수료계)
for s in ['생명보험', '장기', '자동차', '일반']:
    if s in xls2.sheet_names:
        df_raw = pd.read_excel(FILE2, sheet_name=s)
        if '증권번호' in df_raw.columns:
            df_raw['증권번호'] = df_raw['증권번호'].astype(str).str.strip()
            d = get_sum_dict(df_raw, '증권번호', '수수료계')
            for k, v in d.items():
                dict_raw_fee[k] = dict_raw_fee.get(k, 0) + v

# (2) 관리수수료 (지사수수료, FC수수료, 분담금)
sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s]
if sheet_manage:
    df_m = pd.read_excel(FILE2, sheet_name=sheet_manage[0])
    if '증권번호' in df_m.columns:
        df_m['증권번호'] = df_m['증권번호'].astype(str).str.strip()
        
        # 지사수수료
        fee_col = '지사수수료' if '지사수수료' in df_m.columns else df_m.columns[-1]
        dict_manage_fee = get_sum_dict(df_m, '증권번호', fee_col)
        
        # FC수수료
        if 'FC수수료' in df_m.columns:
            dict_fc_fee = get_sum_dict(df_m, '증권번호', 'FC수수료')
            
        # 분담금
        if '분담금' in df_m.columns:
            dict_bundam = get_sum_dict(df_m, '증권번호', '분담금')

# ==========================================
# 2. 파일 1 (통합본) 로드 및 병합
# ==========================================
print("[2] 1번 파일(통합본) 로드 및 병합 적용 중...")
xls1 = pd.ExcelFile(FILE1)
writer = pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl')

for sheet_name in xls1.sheet_names:
    print(f"  - 시트 처리 중: {sheet_name}")
    df1 = pd.read_excel(FILE1, sheet_name=sheet_name)
    
    # 1. A열~X열 까지만 잘라내기 (0번 인덱스 ~ 23번 인덱스 = 24개 컬럼)
    col_limit = min(len(df1.columns), 24)
    df_merged = df1.iloc[:, :col_limit].copy()
    
    if '증권번호' in df_merged.columns:
        df_merged['증권번호_str'] = df_merged['증권번호'].astype(str).str.strip()
        
        # Y열: FC수수료
        df_merged['FC수수료'] = df_merged['증권번호_str'].map(dict_fc_fee).fillna(0)
        
        # Z열: 지사수수료 (= 생명보험등 수수료계 + 관리수수료 지사수수료)
        val_raw = df_merged['증권번호_str'].map(dict_raw_fee).fillna(0)
        val_manage = df_merged['증권번호_str'].map(dict_manage_fee).fillna(0)
        df_merged['지사수수료'] = val_raw + val_manage
        
        # AA열: 분담금
        df_merged['분담금'] = df_merged['증권번호_str'].map(dict_bundam).fillna(0)
        
        # 임시 컬럼 삭제
        df_merged.drop(columns=['증권번호_str'], inplace=True)
    else:
        # 증권번호가 없는 시트일 경우 빈 값으로 추가
        df_merged['FC수수료'] = 0
        df_merged['지사수수료'] = 0
        df_merged['분담금'] = 0

    df_merged.to_excel(writer, sheet_name=sheet_name, index=False)

writer.close()

print("\n" + "="*60)
print(f"✅ 병합 완료! 새로운 파일이 생성되었습니다.")
print(f"📁 저장 위치: {OUTPUT_FILE}")
print("="*60)
