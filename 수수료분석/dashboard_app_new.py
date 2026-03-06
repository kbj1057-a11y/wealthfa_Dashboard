# ==========================================
# 5. 사전 데이터 연산 (렌더링 전 클릭 상태 추적용)
# ==========================================
st.markdown("<h1 style='color:#0B57D0 !important; font-weight:800; font-size:2.5rem;'>웰스FA 26년2월수수료 정밀분석</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B; font-weight:600;'>※ 본 수수료명세서는 1월 영업 업적을 바탕으로 산출된 데이터입니다.</p>", unsafe_allow_html=True)
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

# [업적대시보드 KPI 값]
val_life_hwansan = life_df[is_jan_new]['업적지표1'].sum() 
val_life_premium = life_df[is_jan_new]['업적지표2'].sum() 
val_damage_premium = damage_df[is_jan_new_dmg]['업적지표3'].sum() 

# [업적대시보드 랭킹표 데이터]
l_h_rank = life_df[is_jan_new].groupby('제휴사명')['업적지표1'].sum().reset_index().sort_values('업적지표1', ascending=False)
l_h_rank = l_h_rank[l_h_rank['업적지표1'] > 0]
l_p_rank = life_df[is_jan_new].groupby('제휴사명')['업적지표2'].sum().reset_index().sort_values('업적지표2', ascending=False)
l_p_rank = l_p_rank[l_p_rank['업적지표2'] > 0]
d_p_rank = damage_df[is_jan_new_dmg].groupby('제휴사명')['업적지표3'].sum().reset_index().sort_values('업적지표3', ascending=False)
d_p_rank = d_p_rank[d_p_rank['업적지표3'] > 0]

# [수수료 대시보드용 데이터 분리]
life_new_df = life_df[is_life_new]
life_ret_df = life_df[~is_life_new]
dmg_new_df = damage_df[is_dmg_new]
dmg_ret_df = damage_df[~is_dmg_new]

val_life_new = life_new_df['지사수수료'].sum()
val_life_ret = life_ret_df['지사수수료'].sum()
val_dmg_new = dmg_new_df['지사수수료'].sum()
val_dmg_ret = dmg_ret_df['지사수수료'].sum()

# [수수료 대시보드 제휴사 랭킹 데이터]
l_new_comp = life_new_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
l_new_comp = l_new_comp[l_new_comp['지사수수료'] != 0]
l_ret_comp = life_ret_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
l_ret_comp = l_ret_comp[l_ret_comp['지사수수료'] != 0]

d_new_comp = dmg_new_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_new_comp = d_new_comp[d_new_comp['지사수수료'] != 0]
d_ret_comp = dmg_ret_df.groupby('제휴사명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False)
d_ret_comp = d_ret_comp[d_ret_comp['지사수수료'] != 0]

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

# 2) 상품군 레벨 클릭 확인 (회사 클릭 상태일 때 그 안에 표시되는 상품군 클릭)
if target_scope == '생명 익월' and target_company:
    idx = get_sel(f'sel_life_new_prod_{target_company}')
    if idx is not None and idx < len(l_new_prod):
        target_product = l_new_prod.iloc[idx]['상품군']
elif target_scope == '손해 익월' and target_company:
    idx = get_sel(f'sel_dmg_new_prod_{target_company}')
    if idx is not None and idx < len(d_new_prod):
        target_product = d_new_prod.iloc[idx]['상품군']

# ==========================================
# 7. [상단] 1월 신계약 업적 대시보드 (3-Column)
# ==========================================
st.markdown("<h3 style='color:#1E293B !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #0B57D0;'>🏆 1월 신계약 업적 대시보드 (환산/보험료)</h3>", unsafe_allow_html=True)
col_ach1, col_ach2, col_ach3 = st.columns(3)

with col_ach1:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">생명보험 1월 신계약 환산업적</p>
        <h2 class="kpi-value" style="color:#0B57D0 !important; font-size:1.8rem;">{val_life_hwansan:,.0f} <span style="font-size:1.0rem; color:#64748B;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 신계약 환산 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(l_h_rank.rename(columns={'업적지표1': '환산금액'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_life1")
    st.markdown("</div>", unsafe_allow_html=True)

with col_ach2:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">생명보험 1월 신계약 보험료</p>
        <h2 class="kpi-value" style="color:#10B981 !important; font-size:1.8rem;">{val_life_premium:,.0f} <span style="font-size:1.0rem; color:#64748B;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 신계약 보험료 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(l_p_rank.rename(columns={'업적지표2': '보험료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_life2")
    st.markdown("</div>", unsafe_allow_html=True)

with col_ach3:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-title">손해보험 1월 신계약 보험료</p>
        <h2 class="kpi-value" style="color:#F59E0B !important; font-size:1.8rem;">{val_damage_premium:,.0f} <span style="font-size:1.0rem; color:#64748B;">원</span></h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 손보 보험료 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(d_p_rank.rename(columns={'업적지표3': '총보험료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_ach_dmg1")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 8. [중간] 상세 데이터 테이블 영역 (양면 연동)
# ==========================================
# 타겟 스코프에 맞춰 원본 데이터 세팅
if target_scope == '생명 업적': detail_df = life_df[is_jan_new].copy()
elif target_scope == '손해 업적': detail_df = damage_df[is_jan_new_dmg].copy()
elif target_scope == '생명 익월': detail_df = life_new_df.copy()
elif target_scope == '생명 유지': detail_df = life_ret_df.copy()
elif target_scope == '손해 익월': detail_df = dmg_new_df.copy()
elif target_scope == '손해 유지': detail_df = dmg_ret_df.copy()
else: detail_df = filtered_df.copy()

# 회사 혹은 상품 클릭에 따른 필터링 적용
if target_product and target_company:
    st.markdown(f"<h4 style='color:#0B57D0 !important; font-weight: 700;'>🔎 조회중: [{target_company}]의 [{target_product}] ({target_scope} 부문) 상세 데이터</h3>", unsafe_allow_html=True)
    detail_df = detail_df[(detail_df['제휴사명'] == target_company) & (detail_df['상품군'] == target_product)]
elif target_company:
    st.markdown(f"<h4 style='color:#0B57D0 !important; font-weight: 700;'>🔎 조회중: [{target_company}] 전체 ({target_scope} 부문) 상세 데이터</h3>", unsafe_allow_html=True)
    detail_df = detail_df[detail_df['제휴사명'] == target_company]
else:
    st.markdown("<h4 style='color:#1E293B !important; font-weight: 700;'>📄 웰스FA 전체 필터링 데이터 상세</h3>", unsafe_allow_html=True)
    st.caption("💡 위 업적 표나 아래 수수료 표에서 회사를 클릭하면 이 자리에 상세 내역이 연동됩니다.")

display_cols = ['계약일자_정제', '제휴사명', 'FC명', '지급구분', '상품군', '상품명', '계약자', '업적지표2', '업적지표3', '업적지표1', '지사수수료']
display_df = detail_df[[c for c in display_cols if c in detail_df.columns]].copy()
rename_dict = {'계약일자_정제': '계약일자', '업적지표1': '환산', '업적지표2': '생명_보험료', '업적지표3': '손해_보험료', '지사수수료': '지사수수료(원)'}
display_df.rename(columns=rename_dict, inplace=True)

# 열 숨기기
if target_scope:
    if '생명' in target_scope and '손해_보험료' in display_df.columns:
        display_df = display_df.drop(columns=['손해_보험료'])
    elif '손해' in target_scope:
        if '생명_보험료' in display_df.columns: display_df = display_df.drop(columns=['생명_보험료'])
        if '환산' in display_df.columns: display_df = display_df.drop(columns=['환산'])

st.dataframe(display_df, use_container_width=True, height=400)
st.markdown("---")

# ==========================================
# 9. [하단] 전체 수수료 대시보드 (피라미드 구조)
# ==========================================
st.markdown("<h3 style='color:#1E293B !important; font-weight: 700; padding-left: 5px; border-left: 5px solid #10B981;'>💰 전체 수수료 대시보드 (지사수수료 기준)</h3>", unsafe_allow_html=True)

# 9-1. 피라미드 상단 (총 수수료)
top_col1, top_col2 = st.columns(2)
with top_col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 5px solid #0B57D0; background-color: #F8FAFC; text-align: center;">
        <p class="kpi-title" style="font-size:1.1rem;">🔵 생명보험 총 수수료</p>
        <h2 class="kpi-value" style="color:#0B57D0 !important; font-size:2.8rem;">{val_life_new + val_life_ret:,.0f} <span style="font-size:1.2rem; color:#64748B;">원</span></h2>
        <p style="color:#64748B; margin-top:5px; font-size:0.9rem;">익월(신계약) + 유지 수수료 합산</p>
    </div>
    """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 5px solid #F59E0B; background-color: #F8FAFC; text-align: center;">
        <p class="kpi-title" style="font-size:1.1rem;">🟠 손해보험 총 수수료</p>
        <h2 class="kpi-value" style="color:#F59E0B !important; font-size:2.8rem;">{val_dmg_new + val_dmg_ret:,.0f} <span style="font-size:1.2rem; color:#64748B;">원</span></h2>
        <p style="color:#64748B; margin-top:5px; font-size:0.9rem;">익월(신계약) + 유지 수수료 합산</p>
    </div>
    """, unsafe_allow_html=True)

# 9-2. 피라미드 하단 (4개 상세 분류)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='kpi-card'><p class='kpi-title'>① 생명 익월 수수료</p><h2 class='kpi-value' style='color:#0B57D0 !important; font-size:1.8rem;'>{val_life_new:,.0f} <span style='font-size:1.0rem; color:#64748B;'>원</span></h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='table-container' style='margin-bottom:15px;'><p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(l_new_comp.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_life_new_comp")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if target_scope == '생명 익월' and target_company:
        st.markdown(f"<div class='table-container' style='border: 2px solid #0B57D0;'><p style='font-size:0.9rem; font-weight:bold; color:#0B57D0;'>▸ [{target_company}] 상품군별 (클릭시 중간상세)</p>", unsafe_allow_html=True)
        if len(l_new_prod) > 0:
            st.dataframe(l_new_prod.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_life_new_prod_{target_company}")
        else:
            st.info("해당 회사의 상품군 데이터가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='kpi-card'><p class='kpi-title'>② 생명 유지 수수료</p><h2 class='kpi-value' style='color:#10B981 !important; font-size:1.8rem;'>{val_life_ret:,.0f} <span style='font-size:1.0rem; color:#64748B;'>원</span></h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='table-container'><p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(l_ret_comp.rename(columns={'지사수수료': '유지수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_life_ret_comp")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='kpi-card'><p class='kpi-title'>③ 손해 익월 수수료</p><h2 class='kpi-value' style='color:#F59E0B !important; font-size:1.8rem;'>{val_dmg_new:,.0f} <span style='font-size:1.0rem; color:#64748B;'>원</span></h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='table-container' style='margin-bottom:15px;'><p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(d_new_comp.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_new_comp")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if target_scope == '손해 익월' and target_company:
        st.markdown(f"<div class='table-container' style='border: 2px solid #F59E0B;'><p style='font-size:0.9rem; font-weight:bold; color:#F59E0B;'>▸ [{target_company}] 상품군별 (클릭시 중간상세)</p>", unsafe_allow_html=True)
        if len(d_new_prod) > 0:
            st.dataframe(d_new_prod.rename(columns={'지사수수료': '익월수수료'}), hide_index=True, use_container_width=True, height=150, selection_mode="single-row", on_select="rerun", key=f"sel_dmg_new_prod_{target_company}")
        else:
            st.info("해당 회사의 상품군 데이터가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='kpi-card'><p class='kpi-title'>④ 손해 유지 수수료</p><h2 class='kpi-value' style='color:#8B5CF6 !important; font-size:1.8rem;'>{val_dmg_ret:,.0f} <span style='font-size:1.0rem; color:#64748B;'>원</span></h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='table-container'><p style='font-size:0.9rem; font-weight:bold; color:#475569;'>▸ 제휴사별 (클릭시 중간상세)</p>", unsafe_allow_html=True)
    st.dataframe(d_ret_comp.rename(columns={'지사수수료': '유지수수료'}), hide_index=True, use_container_width=True, height=200, selection_mode="single-row", on_select="rerun", key="sel_dmg_ret_comp")
    st.markdown("</div>", unsafe_allow_html=True)
