import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def disp_dataframe(df, *args, **kwargs):
    # 숫자형 컬럼 포맷팅
    format_dict = {c: "{:,.0f}" for c in df.columns if pd.api.types.is_numeric_dtype(df[c])}
    
    # 마이너스 값에 크림슨 레드(경고/환수) 컬러 적용 함수
    def color_negative_red(val):
        if pd.api.types.is_number(val) and val < 0:
            return 'color: #E63946'
        return ''

    # 스타일 적용
    styled_df = df.style.format(format_dict, na_rep="").map(color_negative_red)
    return st.dataframe(styled_df, *args, **kwargs)

# 1. 페이지 및 탭 타이틀 설정
st.set_page_config(page_title="웰스FA 26년2월수수료 정밀분석", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# 2. VVIP 다크 테마 (Midnight Navy & Gold) & 커스텀 CSS 주입
custom_css = """
<style>
    :root {
        --bg-main: #0A1128;
        --bg-card: #16203B;
        --color-gold: #D4AF37;
        --color-text: #E2E8F0;
        --color-danger: #E63946;
    }

    /* 전체 배경색 강제 지정 */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-main) !important;
        color: var(--color-text) !important;
    }
    
    /* 사이드바 완전 숨김 */
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[kind="header"] {
        display: none !important;
    }
    
    /* 타이틈 인라인 스타일에 간섭하지 않도록 span, p만 정답 구독 */
    p, label, .stMarkdown > div, .stText {
        color: var(--color-text);
        text-shadow: none !important;
    }

    /* ★ 메인 타이틈(h1) 메탈릭 골드 강제주입 ★
       Streamlit의 h1 흰색 오버라이드를 가장 후위 연산자로 완전 차단 */
    .main h1, [data-testid="stMarkdownContainer"] h1 {
        background: linear-gradient(90deg, #BF953F, #FCF6BA, #D4AF37, #FBF5B7, #AA771C) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        color: transparent !important;
        filter: drop-shadow(0px 4px 10px rgba(212,175,55,0.4)) !important;
        text-shadow: none !important;
        font-weight: 900 !important;
    }

    /* ★ 단위 'unit-won' 코드보 사이즈 강제 축소 ★ */
    .unit-won {
        font-size: 14px !important;
        color: #94A3B8 !important;
        font-weight: 400 !important;
    }

    /* KPI 카드 등 컨테이너 배경 */
    .kpi-card {
        background: linear-gradient(180deg, var(--bg-card) 0%, #0A1128 100%) !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5) !important;
        border-radius: 12px !important;
        padding: 36px 28px 28px 28px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 4px solid var(--color-gold) !important;
        overflow: hidden !important;
        text-align: center !important;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .kpi-title {
        color: #A0AEC0 !important; font-weight:700; font-size:1.4rem; margin-bottom:5px;
    }
    
    .kpi-value {
        color: var(--color-gold) !important; font-weight:900; font-size:3.2rem; margin:0;
    }
    
    
    /* 촌스러운 엑셀 격자선 전면 철거 (VVIP 하이엔드) */
    table, th, td, [data-testid="stDataFrame"] > div, .stDataFrame, .stDataFrame > div > div, .stDataFrame > div > div > div {
        border-left: none !important;
        border-right: none !important;
        border-top: none !important;    
    }
    
    th {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    td {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* 흉측한 하얀색 표 전면 개조 (기본 HTML table 적용 시) */
    table {
        width: 100%;
        border-collapse: collapse;
        background-color: var(--bg-card) !important;
        color: var(--color-text) !important;
    }
    th, td {
        background-color: var(--bg-card) !important;
        color: var(--color-text) !important;
        border: none !important;
    }
    th {
        border-bottom: 2px solid var(--color-gold) !important;
        padding: 12px 8px;
        text-align: center;
        font-weight: 700;
    }
    td {
        padding: 10px 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: background-color 0.2s ease;
    }
    tr:hover td {
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    
    
    /* 상세보기 토글 버튼 스타일 (VVIP) */
    .table-toggle-btn {
        background-color: rgba(22, 32, 59, 0.8); /* --bg-card with opacity */
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 500;
        font-size: 1.0rem;
        color: var(--color-text);
        display: inline-block;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: color 0.2s ease, background-color 0.2s ease;
        cursor: pointer;
    }
    
    .table-toggle-btn:hover {
        color: var(--color-gold);
        background-color: rgba(255, 255, 255, 0.05); /* slightly brighten */
    }
    
    .table-toggle-btn::after {
        content: ' ▼';
        font-size: 0.85em;
        margin-left: 6px;
        opacity: 0.8;
    }

    /* 토글 컨테이너 (테이블 박스 상단부 결합용) */
    .table-toggle-container {
        padding: 5px 0 10px 0 !important;
        border: none !important;
        position: relative;
        z-index: 10;
        text-align: left;
    }
    
    /* 스트림릿 컨테이너 간격 여백 당기기 */
    div.stMarkdown:has(.table-toggle-container) {
        margin-bottom: -1rem !important; 
        position: relative;
        z-index: 10;
    }

    /* 스트림릿 테이블(데이터프레임) 스타일 오버라이드 (VVIP 테마) */
    [data-testid="stDataFrame"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        position: relative;
        z-index: 1;
    }
    .stDataFrame {
        color: var(--color-text) !important;
    }
    /* Streamlit data table cells override */
    [data-testid="stDataFrame"] td {
        background-color: transparent !important;
        color: var(--color-text) !important;
    }
    [data-testid="stDataFrame"] th {
        background-color: transparent !important;
        color: var(--color-text) !important;
        border-bottom: 2px solid var(--color-gold) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. 데이터 로드 및 전처리
# ==========================================
@st.cache_data
def load_data():
    file_path = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx"
    
    df_life = pd.read_excel(file_path, sheet_name='생명보험사_202602')
    df_damage = pd.read_excel(file_path, sheet_name='손해보험사_202602')
    
    df_life['보험군'] = '생명보험'
    df_damage['보험군'] = '손해보험'
    
    # 생명보험 지표
    if '환산성적' in df_life.columns:
        df_life['업적지표1'] = df_life['환산성적'] # 생명 환산
    else:
        df_life['업적지표1'] = 0
        
    if '보험료' in df_life.columns:
        df_life['업적지표2'] = df_life['보험료']  # 생명 보험료
    else:
        df_life['업적지표2'] = 0
        
    # 손해보험 지표 (수정보험료 -> 순수 보험료로 변경)
    if '보험료' in df_damage.columns:
        df_damage['업적지표3'] = df_damage['보험료'] # 손해 보험료
    elif '수정보험료' in df_damage.columns: 
        # 보험료 컬럼이 아예 없으면 최후의 보루로만 사용
        df_damage['업적지표3'] = df_damage['수정보험료'] 
    else:
        df_damage['업적지표3'] = 0
        
    df_life['업적지표3'] = 0
    df_damage['업적지표1'] = 0
    df_damage['업적지표2'] = 0

    # 통합 업적지표 (트리맵 등 시각화용 공통 기준값)
    df_life['통합업적'] = df_life['업적지표1'] # 생명은 환산성적 기준
    df_damage['통합업적'] = df_damage['업적지표3'] # 손해는 보험료 기준
        
    common_cols = ['보험군', '제휴사명', 'FC명', '계약자', '상품군', '상품명', '증권번호', '계약일자', '지급구분',
                   '업적지표1', '업적지표2', '업적지표3', '통합업적', 'FC수수료', '지사수수료', '분담금']
    
    life_cols = [c for c in common_cols if c in df_life.columns]
    damage_cols = [c for c in common_cols if c in df_damage.columns]
    
    df_all = pd.concat([df_life[life_cols], df_damage[damage_cols]], ignore_index=True)
    
    # 계약일자 문자열 전처리 (소수점 제거 및 YYYYMMDD 형태 확보)
    if '계약일자' in df_all.columns:
        df_all['계약일자_정제'] = df_all['계약일자'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    else:
        df_all['계약일자_정제'] = '00000000'
    
    num_cols = ['업적지표1', '업적지표2', '업적지표3', '통합업적', 'FC수수료', '지사수수료', '분담금']
    for c in num_cols:
        if c in df_all.columns:
            df_all[c] = pd.to_numeric(df_all[c], errors='coerce').fillna(0)
            
    # PyArrow 에러 방지를 위해 나머지 주요 텍스트 컬럼을 문자열로 강제 고정
    text_cols = ['증권번호', '계약일자', '계약자', 'FC명', '제휴사명', '상품명', '상품군', '지급구분']
    for c in text_cols:
        if c in df_all.columns:
            df_all[c] = df_all[c].astype(str)
            
    # 상품군 결측치 처리
    if '상품군' not in df_all.columns:
        df_all['상품군'] = '분류없음'
    df_all['상품군'] = df_all['상품군'].fillna('분류없음')
    df_all['FC명'] = df_all['FC명'].fillna('알수없음')
    df_all['제휴사명'] = df_all['제휴사명'].fillna('알수없음')

    # 상품군 텍스트 정제 (의미없는 공백 제거)
    df_all['상품군'] = df_all['상품군'].astype(str).str.strip()

    return df_all

df = load_data()

# ==========================================
# 4. 데이터 준비 (사이드바 필터 제거 - 전체 데이터 사용)
# ==========================================
filtered_df = df.copy()  # 사이드바 없이 전체 데이터 그대로 사용

# ==========================================
# 5. 사전 데이터 연산 (렌더링 전 클릭 상태 추적용)
# ==========================================
title_html = """
<div style="margin-bottom: 2rem;">
    <h1 style="
        font-size: 3.5rem; 
        font-weight: 900; 
        color: transparent !important; 
        background: linear-gradient(90deg, #BF953F 0%, #FCF6BA 25%, #D4AF37 50%, #FBF5B7 75%, #AA771C 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent !important; 
        filter: drop-shadow(0px 4px 10px rgba(212, 175, 55, 0.4)); 
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    ">웰스FA 26년 2월 수수료 정밀분석</h1>
    <p style="
        font-size: 14px; 
        color: #94A3B8 !important; 
        font-weight: 500; 
        margin-top: 0;
    ">※ 본 수수료명세서는 1월 영업 업적을 바탕으로 산출된 데이터입니다.</p>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("---")

# 기본 데이터 분리
life_df = filtered_df[filtered_df['보험군'] == '생명보험']
damage_df = filtered_df[filtered_df['보험군'] == '손해보험']

# 👉 수익/유지 등 전반 타겟팅을 위한 조건 (지사수수료 대시보드용)
is_life_new = life_df['지급구분'].astype(str).str.contains('신계약', na=False)
is_dmg_new = damage_df['지급구분'].astype(str).str.contains('신계약', na=False)

# 👉 순수 1월 신계약 업적 분석을 위한 별도 조건 (업적 대시보드용)
is_jan_new = life_df['계약일자_정제'].str.startswith('202601', na=False)
is_dmg_date_match = damage_df['계약일자_정제'].str.startswith('202601', na=False)
is_jan_new_dmg = is_dmg_date_match & is_dmg_new
is_jan_gen_dmg = is_dmg_date_match & (damage_df['지급구분'] == '일반')
is_jan_car_dmg = is_dmg_date_match & (damage_df['지급구분'] == '자동차')

# [업적대시보드 KPI 값]
val_life_hwansan = life_df[is_jan_new]['업적지표1'].sum() 
val_life_premium = life_df[is_jan_new]['업적지표2'].sum() 
val_damage_premium = damage_df[is_jan_new_dmg]['업적지표3'].sum() 
val_damage_gen_premium = damage_df[is_jan_gen_dmg]['업적지표3'].sum() 
val_damage_car_premium = damage_df[is_jan_car_dmg]['업적지표3'].sum() 

# [업적대시보드 랭킹표 데이터]
l_h_rank = life_df[is_jan_new].groupby('제휴사명')['업적지표1'].sum().reset_index().sort_values('업적지표1', ascending=False)
l_h_rank = l_h_rank[l_h_rank['업적지표1'] > 0]
l_p_rank = life_df[is_jan_new].groupby('제휴사명')['업적지표2'].sum().reset_index().sort_values('업적지표2', ascending=False)
l_p_rank = l_p_rank[l_p_rank['업적지표2'] > 0]
d_p_rank = damage_df[is_jan_new_dmg].groupby('제휴사명')['업적지표3'].sum().reset_index().sort_values('업적지표3', ascending=False)
d_p_rank = d_p_rank[d_p_rank['업적지표3'] > 0]
d_p_gen_rank = damage_df[is_jan_gen_dmg].groupby('제휴사명')['업적지표3'].sum().reset_index().sort_values('업적지표3', ascending=False)
d_p_gen_rank = d_p_gen_rank[d_p_gen_rank['업적지표3'] > 0]
d_p_car_rank = damage_df[is_jan_car_dmg].groupby('제휴사명')['업적지표3'].sum().reset_index().sort_values('업적지표3', ascending=False)
d_p_car_rank = d_p_car_rank[d_p_car_rank['업적지표3'] > 0]

# [수수료 대시보드용 데이터 분리]
life_new_df = life_df[is_life_new]
life_ret_df = life_df[~is_life_new]

# 손해보험: 신계약, 유지보수, 기타(일반, 자동차) 구분
# 손해보험: 신계약, 유지보수, 기타(일반, 자동차, 환수) 구분
is_dmg_ret = damage_df['지급구분'].astype(str).str.contains('유지', na=False)
is_dmg_etc = damage_df['지급구분'].astype(str).str.contains('일반|자동차|환수', na=False, regex=True)

dmg_new_df = damage_df[is_dmg_new]
dmg_ret_df = damage_df[is_dmg_ret]
dmg_etc_df = damage_df[is_dmg_etc]

val_life_new = life_new_df['지사수수료'].sum()
val_life_ret = life_ret_df['지사수수료'].sum()
val_dmg_new = dmg_new_df['지사수수료'].sum()
val_dmg_ret = dmg_ret_df['지사수수료'].sum()
val_dmg_etc = dmg_etc_df['지사수수료'].sum()


# [수수료 대시보드 제휴사 랭킹 데이터]
l_new_comp = life_new_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
l_new_comp = l_new_comp[l_new_comp['지사수수료'] != 0]
l_ret_comp = life_ret_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
l_ret_comp = l_ret_comp[l_ret_comp['지사수수료'] != 0]

d_new_comp = dmg_new_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_new_comp = d_new_comp[d_new_comp['지사수수료'] != 0]

d_ret_comp = dmg_ret_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_ret_comp = d_ret_comp[d_ret_comp['지사수수료'] != 0]

d_etc_comp = dmg_etc_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_etc_comp = d_etc_comp[d_etc_comp['지사수수료'] != 0]

# ==========================================
# 6. 클릭(세션 상태) 감지 및 타겟 정보 추출
# ==========================================
target_company = None
target_product = None
target_scope = None

def get_sel(key):
    try:
        rows = st.session_state.get(key, {}).get('selection', {}).get('rows', [])
        return rows[0] if rows else None
    except:
        return None

# 1) 제휴사(회사) 레벨 클릭 확인
if get_sel('sel_ach_life1') is not None:
    target_company = l_h_rank.iloc[get_sel('sel_ach_life1')]['제휴사명']
    target_scope = '생명 업적'
elif get_sel('sel_ach_life2') is not None:
    target_company = l_p_rank.iloc[get_sel('sel_ach_life2')]['제휴사명']
    target_scope = '생명 업적'
elif get_sel('sel_ach_dmg1') is not None:
    target_company = d_p_rank.iloc[get_sel('sel_ach_dmg1')]['제휴사명']
    target_scope = '손해 업적'
elif get_sel('sel_ach_dmg2') is not None:
    target_company = d_p_gen_rank.iloc[get_sel('sel_ach_dmg2')]['제휴사명']
    target_scope = '손해 업적 일반'
elif get_sel('sel_ach_dmg3') is not None:
    target_company = d_p_car_rank.iloc[get_sel('sel_ach_dmg3')]['제휴사명']
    target_scope = '손해 업적 자동차'
elif get_sel('sel_life_new_comp') is not None:
    target_company = l_new_comp.iloc[get_sel('sel_life_new_comp')]['제휴사명']
    target_scope = '생명 익월'
elif get_sel('sel_life_ret_comp') is not None:
    target_company = l_ret_comp.iloc[get_sel('sel_life_ret_comp')]['제휴사명']
    target_scope = '생명 유지'
elif get_sel('sel_dmg_new_comp') is not None:
    target_company = d_new_comp.iloc[get_sel('sel_dmg_new_comp')]['제휴사명']
    target_scope = '손해 익월'
elif get_sel('sel_dmg_ret_comp') is not None:
    target_company = d_ret_comp.iloc[get_sel('sel_dmg_ret_comp')]['제휴사명']
    target_scope = '손해 유지'
elif get_sel('sel_dmg_etc_comp') is not None:
    target_company = d_etc_comp.iloc[get_sel('sel_dmg_etc_comp')]['제휴사명']
    target_scope = '손해 기타'

# [상품군 랭킹 데이터 동적(선택된 제휴사 기반) 생성] - "생보 손보 신계약에만 해당"
l_new_prod_df = life_new_df.copy()
if target_scope == '생명 익월' and target_company:
    l_new_prod_df = life_new_df[life_new_df['제휴사명'] == target_company]
l_new_prod = l_new_prod_df.groupby('상품군')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
l_new_prod = l_new_prod[l_new_prod['지사수수료'] > 0]

d_new_prod_df = dmg_new_df.copy()
if target_scope == '손해 익월' and target_company:
    d_new_prod_df = dmg_new_df[dmg_new_df['제휴사명'] == target_company]
d_new_prod = d_new_prod_df.groupby('상품군')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_new_prod = d_new_prod[d_new_prod['지사수수료'] > 0]

d_etc_prod_df = dmg_etc_df.copy()
if target_scope == '손해 기타' and target_company:
    d_etc_prod_df = dmg_etc_df[dmg_etc_df['제휴사명'] == target_company]
d_etc_prod = d_etc_prod_df.groupby('상품군')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_etc_prod = d_etc_prod[d_etc_prod['지사수수료'] > 0]

# 2) 상품군 레벨 클릭 확인 (회사 클릭 상태일 때 그 안에 표시되는 상품군 클릭)
if target_scope == '생명 익월' and target_company:
    idx = get_sel(f'sel_life_new_prod_{target_company}')
    if idx is not None and idx < len(l_new_prod):
        target_product = l_new_prod.iloc[idx]['상품군']
elif target_scope == '손해 익월' and target_company:
    idx = get_sel(f'sel_dmg_new_prod_{target_company}')
    if idx is not None and idx < len(d_new_prod):
        target_product = d_new_prod.iloc[idx]['상품군']
elif target_scope == '손해 기타' and target_company:
    idx = get_sel(f'sel_dmg_etc_prod_{target_company}')
    if idx is not None and idx < len(d_etc_prod):
        target_product = d_etc_prod.iloc[idx]['상품군']

# ==========================================
# 7. [상단] 1월 업적 대시보드 (5-Column)
# ==========================================
st.markdown("<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>🏆 1월 신계약 및 기타 업적 대시보드 (환산/보험료)</h3>", unsafe_allow_html=True)
col_ach1, col_ach2, col_ach3, col_ach4, col_ach5 = st.columns(5)

with col_ach1:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">생명보험 신계약 환산</p>
        <h2 class="kpi-value" style="color:#D4AF37 !important; font-size:3.0rem; font-weight:800;">{val_life_hwansan:,.0f} <span style="font-size:1.2rem; color:#A0AEC0;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class=\'table-toggle-container\'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
    disp_dataframe(l_h_rank.rename(columns={'업적지표1': '환산금액'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_life1")


with col_ach2:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">생명보험 신계약 보험료</p>
        <h2 class="kpi-value" style="color:#D4AF37 !important; font-size:3.0rem; font-weight:800;">{val_life_premium:,.0f} <span style="font-size:1.2rem; color:#A0AEC0;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class=\'table-toggle-container\'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
    disp_dataframe(l_p_rank.rename(columns={'업적지표2': '보험료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_life2")


with col_ach3:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">손해보험 신계약 보험료</p>
        <h2 class="kpi-value" style="color:#D4AF37 !important; font-size:3.0rem; font-weight:800;">{val_damage_premium:,.0f} <span style="font-size:1.2rem; color:#A0AEC0;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class=\'table-toggle-container\'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
    disp_dataframe(d_p_rank.rename(columns={'업적지표3': '총보험료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_dmg1")


with col_ach4:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">손해보험 일반 보험료</p>
        <h2 class="kpi-value" style="color:#D4AF37 !important; font-size:3.0rem; font-weight:800;">{val_damage_gen_premium:,.0f} <span style="font-size:1.2rem; color:#A0AEC0;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class=\'table-toggle-container\'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
    disp_dataframe(d_p_gen_rank.rename(columns={'업적지표3': '총보험료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_dmg2")


with col_ach5:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">손해보험 자동차 보험료</p>
        <h2 class="kpi-value" style="color:#D4AF37 !important; font-size:3.0rem; font-weight:800;">{val_damage_car_premium:,.0f} <span style="font-size:1.2rem; color:#A0AEC0;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class=\'table-toggle-container\'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
    disp_dataframe(d_p_car_rank.rename(columns={'업적지표3': '총보험료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_dmg3")


st.markdown("---")

# ==========================================
# 8. [중간] 신계약 및 기타 업적 전용 상세데이터
# ==========================================
st.markdown("<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>📊 1월 전체 업적 전용 상세데이터</h3>", unsafe_allow_html=True)
ach_detail_df = life_df[is_jan_new].copy() # Default
ach_scope = ""

if target_scope == '생명 업적': 
    ach_detail_df = life_df[is_jan_new].copy()
    ach_scope = "생명 업적"
elif target_scope == '손해 업적': 
    ach_detail_df = damage_df[is_jan_new_dmg].copy()
    ach_scope = "손해 업적"
elif target_scope == '손해 업적 일반':
    ach_detail_df = damage_df[is_jan_gen_dmg].copy()
    ach_scope = "손해 업적 일반"
elif target_scope == '손해 업적 자동차':
    ach_detail_df = damage_df[is_jan_car_dmg].copy()
    ach_scope = "손해 업적 자동차"
else:
    # Just show all Jan new contracts & etc
    ach_detail_df = pd.concat([life_df[is_jan_new], damage_df[is_jan_new_dmg], damage_df[is_jan_gen_dmg], damage_df[is_jan_car_dmg]])
    ach_scope = "1월 업적 통합"

if target_scope in ['생명 업적', '손해 업적', '손해 업적 일반', '손해 업적 자동차'] and target_company:
    st.markdown(f"<h4 style='color:#D4AF37 !important; font-weight: 700;'>🔎 조회중: [{target_company}] ({ach_scope}) 상세 데이터</h3>", unsafe_allow_html=True)
    ach_detail_df = ach_detail_df[ach_detail_df['제휴사명'] == target_company]
else:
    st.markdown("<h4 style='color:#FFFFFF !important; font-weight: 700;'>📄 1월 업적 데이터(신계약/기타) 전체 상세</h3>", unsafe_allow_html=True)
    st.caption("💡 위 업적 표에서 회사를 클릭하면 이 자리에 해당 회사의 상세 내역이 연동됩니다.")

display_cols_ach = ['계약일자_정제', '제휴사명', 'FC명', '지급구분', '상품군', '상품명', '계약자', '업적지표2', '업적지표3', '업적지표1']
ach_display_df = ach_detail_df[[c for c in display_cols_ach if c in ach_detail_df.columns]].copy()
rename_dict_ach = {'계약일자_정제': '계약일자', '업적지표1': '환산', '업적지표2': '생명_보험료', '업적지표3': '손해_보험료'}
ach_display_df.rename(columns=rename_dict_ach, inplace=True)

if ach_scope == '생명 업적' and '손해_보험료' in ach_display_df.columns:
    ach_display_df = ach_display_df.drop(columns=['손해_보험료'])
elif '손해' in ach_scope:
    if '생명_보험료' in ach_display_df.columns: ach_display_df = ach_display_df.drop(columns=['생명_보험료'])
    if '환산' in ach_display_df.columns: ach_display_df = ach_display_df.drop(columns=['환산'])

disp_dataframe(ach_display_df, use_container_width=True, height=300)
st.markdown("---")

# ==========================================
# 9. [하단] 전체 수수료 대시보드 (피라미드 구조)
# ==========================================
st.markdown("<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>💰 전체 수수료 대시보드 (지사수수료 기준)</h3>", unsafe_allow_html=True)

double_container_css = '''
<style>
    /* double-zone 래퍼 클래스는 빈 div를 생성하므로 삭제하고 kpi-card-zone에 집중합니다. */
    
    .kpi-card-zone {
        background: linear-gradient(180deg, var(--bg-card) 0%, #0A1128 100%) !important;
        border-radius: 12px !important;
        padding: 36px 28px 28px 28px !important;
        /* 사방: 얇은 반투명 선 → Top만 묵직한 골드로 덮어씌움 */
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 4px solid var(--color-gold) !important;
        overflow: hidden !important;
        text-align: center !important;
        margin-bottom: 15px;
        height: 100%;
        position: relative;
    }
    
    .zone-title { color: #A0AEC0 !important; font-weight:700; font-size:1.4rem; margin-bottom:5px; }
    .zone-value { color: var(--color-gold) !important; font-weight:900; font-size:4.0rem; margin:0; }
    /* ① ~ ⑤ 모두 동일한 2.8rem으로 통일 */
    .zone-value-sub { color: var(--color-gold) !important; font-weight:900; font-size:2.8rem; margin:0; }
    .unit-won { font-size: 16px !important; color: #94A3B8 !important; font-weight: 500 !important; }

    /* Top5 FC 버튼 글자 크기 확대 */
    [data-testid="stButton"] button {
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        padding: 0.55rem 0.8rem !important;
        letter-spacing: 0.2px !important;
    }
</style>
'''
st.markdown(double_container_css, unsafe_allow_html=True)

# 9-1. Double Zone 레이아웃 (50:50 분할)
zone_left, spacer, zone_right = st.columns([1, 0.03, 1])

with zone_left:
    # [좌측 최상단]
    st.markdown(f'''
    <div class="kpi-card-zone" style="margin-bottom: 24px;">
        <p class="zone-title" style="font-size:1.4rem;">🔵 생명보험 총 수수료</p>
        <h2 class="zone-value">{val_life_new + val_life_ret:,.0f} <span class="unit-won">원</span></h2>
        <p style="color:#A0AEC0; margin-top:5px; font-size:1.1rem;">익월(신계약) + 유지(환수 포함) 수수료 합산</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # [좌측 하단] 2열 분할
    sub_l1, sub_l2 = st.columns(2)
    with sub_l1:
        st.markdown(f"<div class='kpi-card-zone'><p class='zone-title'>① 생명 익월 수수료</p><h2 class='zone-value-sub'>{val_life_new:,.0f} <span class='unit-won'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(l_new_comp.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_life_new_comp")
        
        if target_scope == '생명 익월' and target_company:
            st.markdown(f"<div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company}] 상품군별 상세 보기</div></div>", unsafe_allow_html=True)
            if len(l_new_prod) > 0:
                disp_dataframe(l_new_prod.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_life_new_prod_{target_company}")
            else:
                st.info("데이터 없음")

    with sub_l2:
        st.markdown(f"<div class='kpi-card-zone'><p class='zone-title'>② 생명 유지(환수포함)</p><h2 class='zone-value-sub'>{val_life_ret:,.0f} <span class='unit-won'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(l_ret_comp.rename(columns={'지사수수료': '유지수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_life_ret_comp")

with zone_right:
    # [우측 최상단]
    st.markdown(f'''
    <div class="kpi-card-zone" style="margin-bottom: 24px;">
        <p class="zone-title" style="font-size:1.4rem;">🟠 손해보험 총 수수료</p>
        <h2 class="zone-value">{val_dmg_new + val_dmg_ret + val_dmg_etc:,.0f} <span class="unit-won">원</span></h2>
        <p style="color:#A0AEC0; margin-top:5px; font-size:1.1rem;">익월(신계약) + 유지 + 기타(일반/차/환수) 합산</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # [우측 하단] 3열 분할
    sub_r1, sub_r2, sub_r3 = st.columns(3)
    with sub_r1:
        st.markdown(f"<div class='kpi-card-zone' style='padding: 24px 10px 10px 10px !important;'><p class='zone-title'>③ 손해 익월</p><h2 class='zone-value-sub'>{val_dmg_new:,.0f} <span class='unit-won'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(d_new_comp.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_new_comp")
        
        if target_scope == '손해 익월' and target_company:
            st.markdown(f"<div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company[:4]}]</div></div>", unsafe_allow_html=True)
            if len(d_new_prod) > 0:
                disp_dataframe(d_new_prod.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_dmg_new_prod_{target_company}")

    with sub_r2:    
        st.markdown(f"<div class='kpi-card-zone' style='padding: 24px 10px 10px 10px !important;'><p class='zone-title'>④ 손해 유지</p><h2 class='zone-value-sub'>{val_dmg_ret:,.0f} <span class='unit-won'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(d_ret_comp.rename(columns={'지사수수료': '유지수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_ret_comp")

    with sub_r3:
        st.markdown(f"<div class='kpi-card-zone' style='padding: 24px 10px 10px 10px !important;'><p class='zone-title'>⑤ 손해 기타</p><h2 class='zone-value-sub'>{val_dmg_etc:,.0f} <span class='unit-won'>원</span></h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='table-toggle-container'><div class='table-toggle-btn'>상세 보기</div></div>", unsafe_allow_html=True)
        disp_dataframe(d_etc_comp.rename(columns={'지사수수료': '기타수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_etc_comp")
        
        if target_scope == '손해 기타' and target_company:
            st.markdown(f"<div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company[:4]}]</div></div>", unsafe_allow_html=True)
            if len(d_etc_prod) > 0:
                disp_dataframe(d_etc_prod.rename(columns={'지사수수료': '기타수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_dmg_etc_prod_{target_company}")

# ==========================================
# 10. [최하단] 수수료 전용 상세데이터
# ==========================================
st.markdown("<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>📊 수수료 전용 상세데이터</h3>", unsafe_allow_html=True)
comm_detail_df = pd.concat([life_new_df, dmg_new_df]) # 기본은 신계약
comm_scope = ""

if target_scope == '생명 익월': 
    comm_detail_df = life_new_df.copy(); comm_scope = target_scope
elif target_scope == '생명 유지': 
    comm_detail_df = life_ret_df.copy(); comm_scope = target_scope
elif target_scope == '손해 익월': 
    comm_detail_df = dmg_new_df.copy(); comm_scope = target_scope
elif target_scope == '손해 유지': 
    comm_detail_df = dmg_ret_df.copy(); comm_scope = target_scope
elif target_scope == '손해 기타': 
    comm_detail_df = dmg_etc_df.copy(); comm_scope = target_scope
else:
    # 전체 수수료
    comm_detail_df = filtered_df.copy()

if comm_scope:
    if target_product and target_company:
        st.markdown(f"<h4 style='color:#D4AF37 !important; font-weight: 700;'>🔎 조회중: [{target_company}]의 [{target_product}] ({comm_scope} 부문) 상세 데이터</h3>", unsafe_allow_html=True)
        comm_detail_df = comm_detail_df[(comm_detail_df['제휴사명'] == target_company) & (comm_detail_df['상품군'] == target_product)]
    elif target_company:
        st.markdown(f"<h4 style='color:#D4AF37 !important; font-weight: 700;'>🔎 조회중: [{target_company}] 전체 ({comm_scope} 부문) 상세 데이터</h3>", unsafe_allow_html=True)
        comm_detail_df = comm_detail_df[comm_detail_df['제휴사명'] == target_company]
else:
    st.markdown("<h4 style='color:#FFFFFF !important; font-weight: 700;'>📄 웰스FA 전체 수수료 데이터 상세</h3>", unsafe_allow_html=True)
    st.caption("💡 위 수수료 표에서 제휴사 또는 상품군을 클릭하면 이 자리에 상세 내역이 연동됩니다.")

display_cols_comm = ['계약일자_정제', '제휴사명', 'FC명', '지급구분', '상품군', '상품명', '계약자', '업적지표2', '업적지표3', '업적지표1', '지사수수료']
comm_display_df = comm_detail_df[[c for c in display_cols_comm if c in comm_detail_df.columns]].copy()
rename_dict_comm = {'계약일자_정제': '계약일자', '업적지표1': '환산', '업적지표2': '생명_보험료', '업적지표3': '손해_보험료', '지사수수료': '지사수수료(원)'}
comm_display_df.rename(columns=rename_dict_comm, inplace=True)

if comm_scope:
    if '생명' in comm_scope and '손해_보험료' in comm_display_df.columns:
        comm_display_df = comm_display_df.drop(columns=['손해_보험료'])
    elif '손해' in comm_scope:
        if '생명_보험료' in comm_display_df.columns: comm_display_df = comm_display_df.drop(columns=['생명_보험료'])
        if '환산' in comm_display_df.columns: comm_display_df = comm_display_df.drop(columns=['환산'])

disp_dataframe(comm_display_df, use_container_width=True, height=400)

st.markdown("---")

# ==========================================
# 11. [최하단] 5개 부문별 지사수수료 기여 Top 5 FC
# ==========================================

# ── 손보 일반만 별도 추출
dmg_gen_only_df = damage_df[damage_df['지급구분'].astype(str).str.contains('일반', na=False)]

# ── 부문별 데이터 매핑 (dialog에서 FC 클릭 시 참조)
TOP5_DF_MAP = {
    '생보_신계약': ('🔵 생보 신계약', life_new_df),
    '생보_유지':   ('🟢 생보 유지',   life_ret_df),
    '손보_신계약': ('🟠 손보 신계약', dmg_new_df),
    '손보_유지':   ('🟣 손보 유지',   dmg_ret_df),
    '손보_일반':   ('⚪ 손보 일반',   dmg_gen_only_df),
}

# ── 세션 초기화
if 'top5_modal_fc' not in st.session_state:
    st.session_state.top5_modal_fc = None
if 'top5_modal_scope' not in st.session_state:
    st.session_state.top5_modal_scope = None

# ── @st.dialog: FC 계약 상세 팝업
@st.dialog("📋 계약 상세 내역", width="large")
def show_fc_detail_popup():
    fc_name  = st.session_state.top5_modal_fc
    scope_key = st.session_state.top5_modal_scope
    label, df_source = TOP5_DF_MAP.get(scope_key, ('', pd.DataFrame()))

    st.markdown(f"""
    <div style='margin-bottom:1rem;'>
        <span style='color:#D4AF37; font-weight:900; font-size:1.3rem;'>👤 {fc_name}</span>
        <span style='color:#64748B; font-size:0.9rem; margin-left:10px;'>— {label} 부문</span>
    </div>
    """, unsafe_allow_html=True)

    if df_source.empty:
        st.warning("데이터가 없습니다.")
        return

    # ── 수수료 전용 상세데이터와 동일한 컬럼 구성
    detail = df_source[df_source['FC명'] == fc_name].copy()
    display_cols = ['계약일자_정제', '제휴사명', 'FC명', '지급구분', '상품군', '상품명',
                    '계약자', '업적지표2', '업적지표3', '업적지표1', '지사수수료']
    detail_disp = detail[[c for c in display_cols if c in detail.columns]].copy()
    rename_dict = {
        '계약일자_정제': '계약일자', '업적지표1': '환산',
        '업적지표2': '생명_보험료', '업적지표3': '손해_보험료',
        '지사수수료': '지사수수료(원)'
    }
    detail_disp.rename(columns=rename_dict, inplace=True)

    # 부문에 맞게 불필요 컬럼 제거
    if '생보' in label:
        if '손해_보험료' in detail_disp.columns:
            detail_disp = detail_disp.drop(columns=['손해_보험료'])
    else:
        if '생명_보험료' in detail_disp.columns:
            detail_disp = detail_disp.drop(columns=['생명_보험료'])
        if '환산' in detail_disp.columns:
            detail_disp = detail_disp.drop(columns=['환산'])

    # ── 요약 KPI (건수 / 지사수수료 합계)
    total_fee = detail['지사수수료'].sum() if '지사수수료' in detail.columns else 0
    k1, k2 = st.columns(2)
    k1.metric("📋 계약건수", f"{len(detail)}건")
    k2.metric("💰 지사수수료 합계", f"{int(total_fee/10000):,}만원")

    st.markdown("<br>", unsafe_allow_html=True)
    disp_dataframe(detail_disp, use_container_width=True, hide_index=True, height=400)

# ── dialog 트리거: 버튼 클릭 후 rerun 시 팝업 호출
if st.session_state.top5_modal_fc:
    show_fc_detail_popup()
    st.session_state.top5_modal_fc = None
    st.session_state.top5_modal_scope = None

# ── 섹션 헤더
st.markdown("""
<h3 style='color:#FFFFFF !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #D4AF37;'>
👑 부문별 지사수수료 기여 Top 5 FC
</h3>
<p style='color:#94A3B8; font-size:0.9rem; margin-top:-0.3rem; margin-bottom:1.2rem;'>
각 부문에서 지사수수료를 가장 많이 창출한 FC 상위 5명입니다. <b style='color:#D4AF37;'>이름을 클릭</b>하면 계약 상세내역이 팝업으로 표시됩니다.
</p>
""", unsafe_allow_html=True)

# ── 메달 설정
MEDAL_ICONS   = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
MEDAL_COLORS  = ["#D4AF37", "#C0C0C0", "#CD7F32", "#94A3B8", "#94A3B8"]

def render_top5_card(title, color_accent, scope_key, fee_col='지사수수료'):
    """지사수수료 기준 상위 5명 FC를 버튼 방식으로 렌더링 (클릭 → 팝업)."""
    _, df_source = TOP5_DF_MAP.get(scope_key, ('', pd.DataFrame()))

    st.markdown(f"""
    <div style='
        background: linear-gradient(180deg, #16203B 0%, #0A1128 100%);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
        border-top: 4px solid {color_accent};
        padding: 16px 14px 10px 14px;
        margin-bottom: 4px;
    '>
        <p style='color:#A0AEC0; font-weight:700; font-size:0.9rem;
                  margin-bottom:10px; letter-spacing:0.5px;'>{title}</p>
    </div>
    """, unsafe_allow_html=True)

    if df_source.empty or fee_col not in df_source.columns:
        st.markdown("<p style='color:#475569; font-size:0.85rem;'>데이터 없음</p>",
                    unsafe_allow_html=True)
        return

    top5 = (
        df_source.groupby('FC명')[fee_col]
        .sum().reset_index()
        .sort_values(fee_col, ascending=False)
        .head(5).reset_index(drop=True)
    )

    for i, row in top5.iterrows():
        man_val    = int(row[fee_col] / 10000)
        icon       = MEDAL_ICONS[i]
        name_color = MEDAL_COLORS[i]
        fc_name    = row['FC명']

        col_btn, col_amt = st.columns([3, 2])
        with col_btn:
            # FC 이름을 버튼으로 — 클릭 시 세션에 저장 후 rerun
            btn_key = f"top5_btn_{scope_key}_{i}_{fc_name}"
            if st.button(
                f"{icon}  {fc_name}",
                key=btn_key,
                use_container_width=True,
            ):
                st.session_state.top5_modal_fc    = fc_name
                st.session_state.top5_modal_scope = scope_key
                st.rerun()
        with col_amt:
            st.markdown(
                f"<p style='color:#E2E8F0; font-weight:900; font-size:0.9rem;"
                f"text-align:right; margin:0; padding-top:6px;'>"
                f"{man_val:,}<span style='color:#64748B; font-size:0.72rem;'>만원</span></p>",
                unsafe_allow_html=True
            )

# ── 5컬럼 렌더링
c1, c2, c3, c4, c5 = st.columns(5)
with c1: render_top5_card("🔵 생보 신계약", "#3B82F6", "생보_신계약")
with c2: render_top5_card("🟢 생보 유지",   "#10B981", "생보_유지")
with c3: render_top5_card("🟠 손보 신계약", "#F59E0B", "손보_신계약")
with c4: render_top5_card("🟣 손보 유지",   "#8B5CF6", "손보_유지")
with c5: render_top5_card("⚪ 손보 일반",   "#94A3B8", "손보_일반")

st.markdown("""
<div style='text-align:center; color:#334155; font-size:0.72rem; margin-top:3rem; padding:1rem;
border-top:1px solid rgba(255,255,255,0.04);'>
웰스FA 수수료 정밀분석 대시보드 · Powered by Antigravity
</div>
""", unsafe_allow_html=True)
