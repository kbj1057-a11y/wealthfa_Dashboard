import pandas as pd
import sys
import warnings
warnings.filterwarnings('ignore')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FILE1 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227수수료_생손보통합_v3.xlsx"
FILE2 = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\260227지사장수수료상세내역.xlsx"
OUTPUT_FILE = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx"

print("="*80)
print("1번, 2번 파일 병합 (증권번호당 1줄 압축 + 환산성적 살리기 + 3대 수수료 추가)")
print("="*80)

# ==========================================
# 1. 파일 2 (상세내역) 데이터사전 만들기
# ==========================================
print("[1] 2번 파일(상세내역) 로드 및 증권번호별 데이터 딕셔너리 생성 중...")
xls2 = pd.ExcelFile(FILE2)

def get_sum_dict(df, id_col, val_col):
    if id_col in df.columns and val_col in df.columns:
        df[val_col] = pd.to_numeric(df[val_col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df.groupby(id_col)[val_col].sum().to_dict()
    return {}

def normalize_id(series):
    """증권번호 문자열 변환 및 숨겨진 .0 소수점 꼬리 제거"""
    return series.astype(str).str.strip().str.replace(r'\.0$', '', regex=True)

dict_raw_fee = {}
for s in ['생명보험', '장기', '자동차', '일반']:
    if s in xls2.sheet_names:
        df_raw = pd.read_excel(FILE2, sheet_name=s)
        if '증권번호' in df_raw.columns:
            df_raw['증권번호'] = normalize_id(df_raw['증권번호'])
            fee_col = '수수료계' if '수수료계' in df_raw.columns else None
            if fee_col:
                d = get_sum_dict(df_raw, '증권번호', fee_col)
                for k, v in d.items():
                    dict_raw_fee[k] = dict_raw_fee.get(k, 0) + v

dict_manage_fee = {}
dict_fc_fee = {}
dict_bundam = {}

sheet_manage = [s for s in xls2.sheet_names if '관리수수료' in s]
if sheet_manage:
    df_m = pd.read_excel(FILE2, sheet_name=sheet_manage[0])
    if '증권번호' in df_m.columns:
        df_m['증권번호'] = normalize_id(df_m['증권번호'])
        
        # 지사수수료
        fee_col = '지사수수료' if '지사수수료' in df_m.columns else None
        if not fee_col:
            candidate = [c for c in df_m.columns if '지사' in str(c) and ('수수료' in str(c) or '수당' in str(c))]
            fee_col = candidate[0] if candidate else df_m.columns[-1]
        dict_manage_fee = get_sum_dict(df_m, '증권번호', fee_col)
        
        # FC수수료
        if 'FC수수료' in df_m.columns:
            dict_fc_fee = get_sum_dict(df_m, '증권번호', 'FC수수료')
            
        # 분담금
        if '분담금' in df_m.columns:
            dict_bundam = get_sum_dict(df_m, '증권번호', '분담금')

# ==========================================
# 2. 파일 1 (통합본) 로드 및 압축 병합
# ==========================================
print("[2] 1번 파일(통합본) 로드 및 압축(Group by) 병합 중...")
xls1 = pd.ExcelFile(FILE1)
writer = pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl')

def is_numeric_col(col_name):
    """금액 합산(+)을 해야 할 컬럼명 판별기 (엄격한 기준 적용)"""
    col_name = str(col_name)
    
    # 1. 명확한 금액/수수료성 단어
    includes = ['보험료', '수수료', '수당', '금액', '합계', '환산', '실적', 'TP', '지급액']
    if any(x in col_name for x in includes):
        return True
        
    # 2. '계' (수수료계 등 독립된 합계 지표일 때, 계약자는 제외하기 위해 exact match 또는 확실한 경우)
    if col_name == '계' or col_name.endswith('계'):
        # '계약자' 등은 '계'로 끝나지 않으므로 안전함
        return True
        
    # 3. 순수 숫자 (1, 2, 3차 회차수당 컬럼)
    if col_name.isdigit():
        return True
        
    # 4. 차년도/회차별 명칭 (초회, 1차년, 1차상 등)
    if '차년' in col_name or '차월' in col_name or '초회' in col_name or '차상' in col_name:
        return True
        
    return False

for sheet_name in xls1.sheet_names:
    print(f"  - 시트 1줄 압축 처리 중: {sheet_name}")
    df1 = pd.read_excel(FILE1, sheet_name=sheet_name)
    
    if '증권번호' not in df1.columns:
        df1.to_excel(writer, sheet_name=sheet_name, index=False)
        continue
        
    df1['증권번호'] = normalize_id(df1['증권번호'])
    
    # 1. 남길 컬럼 식별: A열 ~ X열 (Index 0 ~ 23)
    col_limit = min(len(df1.columns), 24)
    cols_to_keep = list(df1.columns[:col_limit])
    
    # 2. Y열: 환산성적 또는 수정보험료 타겟팅
    target_y = None
    new_y_name = "Y열_핵심지표"
    
    if '생명' in sheet_name:
        y_cands = [c for c in df1.columns if '환산성적' in c or 'TP' in c]
        if y_cands:
            target_y = y_cands[0]
            new_y_name = "환산성적"
    else:
        y_cands = [c for c in df1.columns if '수정보험료' in c or '신월정산' in c or '환산실적' in c]
        if y_cands:
            target_y = y_cands[0]
            new_y_name = "수정보험료"
            
    # 타겟 Y열을 보존 리스트에 추가 (A~X에 없으면)
    if target_y and target_y not in cols_to_keep:
        cols_to_keep.append(target_y)
        
    df_sub = df1[cols_to_keep].copy()
    
    # 3. 압축(Groupby) 규칙 설정
    agg_rules = {}
    for c in cols_to_keep:
        if c == '증권번호':
            continue
        if is_numeric_col(c):
            # 숫자로 변환 후 합산(+) 처리
            df_sub[c] = pd.to_numeric(df_sub[c].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            agg_rules[c] = 'sum'
        else:
            # 텍스트는 제일 첫 번째 행 데이터 남기기
            agg_rules[c] = 'first'
            
    # ★ 증권번호 1개당 무조건 1줄로 압축 (뻥튀기 차단)
    df_grouped = df_sub.groupby('증권번호').agg(agg_rules).reset_index()
    
    # 원래 컬럼 순서 복구
    df_grouped = df_grouped[cols_to_keep]
    
    # 통일된 이름으로 Y열 이름 변경
    if target_y:
        df_grouped.rename(columns={target_y: new_y_name}, inplace=True)
        
    # 4. Z, AA, AB 열 (2번 파일 데이터 매핑)
    df_grouped['FC수수료'] = df_grouped['증권번호'].map(dict_fc_fee).fillna(0)
    
    val_raw = df_grouped['증권번호'].map(dict_raw_fee).fillna(0)
    val_manage = df_grouped['증권번호'].map(dict_manage_fee).fillna(0)
    df_grouped['지사수수료'] = val_raw + val_manage
    
    df_grouped['분담금'] = df_grouped['증권번호'].map(dict_bundam).fillna(0)
    
    # 저장
    df_grouped.to_excel(writer, sheet_name=sheet_name, index=False)

writer.close()

print("\n" + "="*80)
print(f"✅ 무결점 압축 병합 완료! 새로운 파일이 생성되었습니다.")
print(f"📁 저장 위치: {OUTPUT_FILE}")
print("="*80)
