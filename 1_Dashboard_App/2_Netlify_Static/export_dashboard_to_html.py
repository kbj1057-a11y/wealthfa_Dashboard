import pandas as pd
import json

def load_data():
    file_path = r"G:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx"
    df_life = pd.read_excel(file_path, sheet_name='생명보험사_202602')
    df_damage = pd.read_excel(file_path, sheet_name='손해보험사_202602')
    
    df_life['보험군'] = '생명보험'
    df_damage['보험군'] = '손해보험'
    
    df_life['업적지표1'] = df_life['환산성적'] if '환산성적' in df_life.columns else 0
    df_life['업적지표2'] = df_life['보험료'] if '보험료' in df_life.columns else 0
    df_damage['업적지표3'] = df_damage['보험료'] if '보험료' in df_damage.columns else (df_damage['수정보험료'] if '수정보험료' in df_damage.columns else 0)
        
    df_life['업적지표3'] = 0
    df_damage['업적지표1'] = 0
    df_damage['업적지표2'] = 0

    common_cols = ['보험군', '제휴사명', 'FC명', '계약자', '상품군', '상품명', '증권번호', '계약일자', '지급구분',
                   '업적지표1', '업적지표2', '업적지표3', 'FC수수료', '지사수수료']
    val_cols = [c for c in common_cols if c in df_life.columns or c in df_damage.columns]
    
    df_all = pd.concat([df_life[df_life.columns.intersection(val_cols)], 
                        df_damage[df_damage.columns.intersection(val_cols)]], ignore_index=True)
    
    df_all['계약일자_정제'] = df_all['계약일자'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip() if '계약일자' in df_all.columns else '00000000'
    
    for c in ['업적지표1', '업적지표2', '업적지표3', 'FC수수료', '지사수수료']:
        if c in df_all.columns: df_all[c] = pd.to_numeric(df_all[c], errors='coerce').fillna(0)
            
    for c in ['증권번호', '계약일자_정제', '계약자', 'FC명', '제휴사명', '상품명', '상품군', '지급구분']:
        if c in df_all.columns: df_all[c] = df_all[c].astype(str).fillna('-')
            
    df_all['상품군'] = df_all['상품군'].replace('nan', '분류없음').str.strip()
    df_all['FC명'] = df_all['FC명'].replace('nan', '알수없음')
    df_all['제휴사명'] = df_all['제휴사명'].replace('nan', '알수없음')
    return df_all

df = load_data()

life_df = df[df['보험군'] == '생명보험']
damage_df = df[df['보험군'] == '손해보험']

is_life_new = life_df['지급구분'].str.contains('신계약', na=False)
is_dmg_new = damage_df['지급구분'].str.contains('신계약', na=False)

is_jan_new = life_df['계약일자_정제'].str.startswith('202601', na=False)
is_dmg_date_match = damage_df['계약일자_정제'].str.startswith('202601', na=False)

life_new_df = life_df[is_life_new]
life_ret_df = life_df[~is_life_new]
dmg_new_df = damage_df[is_dmg_new]
dmg_ret_df = damage_df[damage_df['지급구분'].str.contains('유지', na=False)]
dmg_etc_df = damage_df[damage_df['지급구분'].str.contains('일반|자동차|환수', na=False, regex=True)]
dmg_gen_only_df = damage_df[damage_df['지급구분'].str.contains('일반', na=False)]

def get_kpi(df_src, cond, col):
    return df_src[cond][col].sum() if cond is not None else df_src[col].sum()

val_life_hwansan = get_kpi(life_df, is_jan_new, '업적지표1')
val_life_premium = get_kpi(life_df, is_jan_new, '업적지표2')
val_dmg_premium = get_kpi(damage_df, is_dmg_date_match & is_dmg_new, '업적지표3')
val_dmg_gen_premium = get_kpi(damage_df, is_dmg_date_match & (damage_df['지급구분']=='일반'), '업적지표3')
val_dmg_car_premium = get_kpi(damage_df, is_dmg_date_match & (damage_df['지급구분']=='자동차'), '업적지표3')

val_life_new = life_new_df['지사수수료'].sum()
val_life_ret = life_ret_df['지사수수료'].sum()
val_dmg_new = dmg_new_df['지사수수료'].sum()
val_dmg_ret = dmg_ret_df['지사수수료'].sum()
val_dmg_etc = dmg_etc_df['지사수수료'].sum()

def get_rank(df_src, val_col):
    df_grp = df_src.groupby('제휴사명')[val_col].sum().reset_index()
    return df_grp[df_grp[val_col] > 0].sort_values(val_col, ascending=False)

def to_html_table(df_grp, val_col, target_scope):
    if df_grp.empty: return "<p style='color:#64748B;'>데이터 없음</p>"
    html = f'''<div class="table-toggle-btn" onclick="openCompModal('{target_scope}')">제휴사별 상세 보기 ▼</div>'''
    html += '<div class="table-container"><table>'
    for _, row in df_grp.iterrows():
        comp, val = row['제휴사명'], row[val_col]
        color_st = 'color:#E63946;' if val < 0 else ''
        html += f'<tr onclick="openDetailModal(&quot;{target_scope}&quot;, &quot;{comp}&quot;, null)" style="cursor:pointer;"><td style="text-align:left;">{comp}</td><td style="text-align:right; {color_st}">{val:,.0f}</td></tr>'
    html += '</table></div>'
    return html

def to_top5_html(title, color, scope_df, target_scope):
    html = f'<div class="top5-card" style="border-top-color:{color};"><div class="top5-title" style="color:#E2E8F0; font-size:1.15rem; font-weight:800;">{title}</div>'
    if scope_df.empty: return html + "<p style='color:#64748B;'>데이터 없음</p></div>"
    
    top5 = scope_df.groupby('FC명')['지사수수료'].sum().reset_index().sort_values('지사수수료', ascending=False).head(5)
    medals, colors = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"], ["#D4AF37", "#C0C0C0", "#CD7F32", "#94A3B8", "#94A3B8"]
    
    for i, row in top5.reset_index(drop=True).iterrows():
        man_val, fc = int(row['지사수수료'] / 10000), row['FC명']
        bg = "rgba(212,175,55,0.08)" if i == 0 else "rgba(255,255,255,0.02)"
        border = "1px solid rgba(212,175,55,0.25)" if i == 0 else "1px solid rgba(255,255,255,0.04)"
        html += f'''
        <div class="top5-row" style="background:{bg}; border:{border}; cursor:pointer;" onclick="openDetailModal(&quot;{target_scope}&quot;, null, &quot;{fc}&quot;)">
            <span style="font-size:1.1rem;">{medals[i]}</span>
            <span style="flex:1; margin-left:10px; color:{colors[i]}; font-weight:700; font-size:1.05rem;">{fc}</span>
            <span style="color:#E2E8F0; font-weight:900;">{man_val:,}<span style="color:#64748B; font-size:0.75rem;">만원</span></span>
        </div>'''
    return html + '</div>'

# JS로 넘길 전체 데이터 가공 (용량 최적화)
export_cols = ['보험군', '제휴사명', 'FC명', '계약자', '상품군', '상품명', '계약일자_정제', '지급구분', '업적지표1', '업적지표2', '업적지표3', '지사수수료']
df_json = df[export_cols].rename(columns={'계약일자_정제': '계약일자'})
json_data = df_json.to_json(orient='records', force_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>웰스FA 26년 2월 수수료 정밀분석</title>
    <style>
        :root {{ --bg-main: #0A1128; --bg-card: #16203B; --color-gold: #D4AF37; --color-text: #E2E8F0; }}
        body {{ background: var(--bg-main); color: var(--color-text); font-family: 'Pretendard', sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        h1 {{ font-size: 3.5rem; font-weight: 900; background: linear-gradient(90deg, #BF953F, #FCF6BA, #D4AF37, #FBF5B7, #AA771C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0px 4px 10px rgba(212,175,55,0.4)); margin-bottom: 0.5rem; }}
        hr {{ border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 30px 0; }}
        .grid-5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; }}
        
        /* 전체 수수료 간격 및 디자인 Streamlit 완벽 대응 */
        .double-zone-wrapper {{ display: flex; gap: 3%; margin-top:20px; }}
        .zone-half {{ flex: 1; display: flex; flex-direction: column; gap: 15px; }}
        .zone-inner-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; height: 100%; }}
        .zone-inner-grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; height: 100%; }}

        .kpi-card, .kpi-card-zone {{
            background: linear-gradient(180deg, var(--bg-card) 0%, #0A1128 100%);
            border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);
            border-top: 4px solid var(--color-gold);
            padding: 24px 20px; text-align: center;
        }}
        .kpi-title {{ color: #A0AEC0; font-weight:700; font-size:1.2rem; margin:0 0 10px 0; }}
        .kpi-value-small {{ color: var(--color-gold); font-weight:900; font-size:2.4rem; margin:0; line-height:1.2; }}
        
        .zone-title {{ color: #A0AEC0; font-weight:700; font-size:1.4rem; margin:0 0 5px 0; }}
        .zone-value {{ color: var(--color-gold); font-weight:900; font-size:4.0rem; margin:0; }}
        .zone-value-sub {{ color: var(--color-gold); font-weight:900; font-size:2.8rem; margin:0; }}
        .unit-won {{ font-size: 16px; color: #94A3B8; font-weight: 500; }}

        .table-toggle-btn {{ background: rgba(22,32,59,0.8); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 16px; color: var(--color-text); cursor: pointer; text-align: left; font-weight: 500; margin-bottom: 12px; font-size:1rem; }}
        .table-toggle-btn:hover {{ color: var(--color-gold); background: rgba(255,255,255,0.05); }}
        
        .table-container {{ max-height: 200px; overflow-y: auto; background: transparent; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        td {{ padding: 8px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        tr:hover td {{ background: rgba(255,255,255,0.05); }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 10px; }}

        .top5-card {{ background: linear-gradient(180deg, #16203B, #0A1128); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); border-top: 4px solid; padding: 16px 14px; margin-bottom: 4px; }}
        .top5-row:hover {{ filter: brightness(1.2); }}

        /* Modal Styles */
        #modalOverlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center; }}
        #modalContent {{ background: #0A1128; border: 1px solid var(--color-gold); border-radius: 12px; width: 90%; max-width: 1200px; max-height: 85vh; display: flex; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }}
        .modal-header {{ padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center; }}
        .modal-body {{ padding: 20px; overflow-y: auto; flex: 1; }}
        .modal-close {{ background: none; border: none; color: #FFF; font-size: 1.5rem; cursor: pointer; }}
        #modalTable th {{ position: sticky; top: 0; background: #16203B; color: #A0AEC0; padding: 12px; border-bottom: 2px solid var(--color-gold); }}
        #modalTable td {{ text-align: center; }}
        .metric-box {{ background: #16203B; border-radius: 8px; padding: 15px; text-align: center; flex: 1; border: 1px solid rgba(255,255,255,0.05); }}
    </style>
</head>
<body>
<div class="container">
    <h1>웰스FA 26년 2월 수수료 정밀분석</h1>
    <p style="color:#94A3B8;">※ 본 수수료명세서는 1월 영업 업적을 바탕으로 산출된 데이터입니다.</p>
    <hr>
    
    <div style="color:#FFF; font-weight:700; font-size:1.5rem; border-left:5px solid #D4AF37; padding-left:10px; margin-bottom:20px;">🏆 1월 신계약 및 기타 업적 대시보드 (환산/보험료)</div>
    <div class="grid-5">
        <div class="kpi-card"><p class="kpi-title">생명보험 신계약 환산</p><p class="kpi-value-small">{val_life_hwansan:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(life_df[is_jan_new], '업적지표1'), '업적지표1', 'ach_life_h')}</div>
        <div class="kpi-card"><p class="kpi-title">생명보험 신계약 보험료</p><p class="kpi-value-small">{val_life_premium:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(life_df[is_jan_new], '업적지표2'), '업적지표2', 'ach_life_p')}</div>
        <div class="kpi-card"><p class="kpi-title">손해보험 신계약 보험료</p><p class="kpi-value-small">{val_damage_premium:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(damage_df[is_dmg_date_match & is_dmg_new], '업적지표3'), '업적지표3', 'ach_dmg_new')}</div>
        <div class="kpi-card"><p class="kpi-title">손해보험 일반 보험료</p><p class="kpi-value-small">{val_damage_gen_premium:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(damage_df[is_dmg_date_match & (damage_df['지급구분']=='일반')], '업적지표3'), '업적지표3', 'ach_dmg_gen')}</div>
        <div class="kpi-card"><p class="kpi-title">손해보험 자동차 보험료</p><p class="kpi-value-small">{val_damage_car_premium:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(damage_df[is_dmg_date_match & (damage_df['지급구분']=='자동차')], '업적지표3'), '업적지표3', 'ach_dmg_car')}</div>
    </div>
    
    <hr>
    <div style="color:#FFF; font-weight:700; font-size:1.5rem; border-left:5px solid #D4AF37; padding-left:10px; margin-bottom:20px;">💰 전체 수수료 대시보드 (지사수수료 기준)</div>
    <div class="double-zone-wrapper">
        <div class="zone-half">
            <div class="kpi-card-zone"><p class="zone-title">🔵 생명보험 총 수수료</p><p class="zone-value">{val_life_new + val_life_ret:,.0f} <span class="unit-won">원</span></p><p style="color:#A0AEC0; margin-top:5px;">익월(신계약) + 유지(환수 포함) 수수료 합산</p></div>
            <div class="zone-inner-grid-2">
                <div class="kpi-card-zone" style="padding: 24px 15px;"><p class="zone-title">① 생명 익월 수수료</p><p class="zone-value-sub">{val_life_new:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(life_new_df, '지사수수료'), '지사수수료', 'fee_life_new')}</div>
                <div class="kpi-card-zone" style="padding: 24px 15px;"><p class="zone-title">② 생명 유지(환수포함)</p><p class="zone-value-sub">{val_life_ret:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(life_ret_df, '지사수수료'), '지사수수료', 'fee_life_ret')}</div>
            </div>
        </div>
        <div class="zone-half">
            <div class="kpi-card-zone"><p class="zone-title">🟠 손해보험 총 수수료</p><p class="zone-value">{val_dmg_new + val_dmg_ret + val_dmg_etc:,.0f} <span class="unit-won">원</span></p><p style="color:#A0AEC0; margin-top:5px;">익월(신계약) + 유지 + 기타(일반/차/환수) 합산</p></div>
            <div class="zone-inner-grid-3">
                <div class="kpi-card-zone" style="padding: 24px 10px;"><p class="zone-title">③ 손해 익월</p><p class="zone-value-sub">{val_dmg_new:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(dmg_new_df, '지사수수료'), '지사수수료', 'fee_dmg_new')}</div>
                <div class="kpi-card-zone" style="padding: 24px 10px;"><p class="zone-title">④ 손해 유지</p><p class="zone-value-sub">{val_dmg_ret:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(dmg_ret_df, '지사수수료'), '지사수수료', 'fee_dmg_ret')}</div>
                <div class="kpi-card-zone" style="padding: 24px 10px;"><p class="zone-title">⑤ 손해 기타</p><p class="zone-value-sub">{val_dmg_etc:,.0f} <span class="unit-won">원</span></p>{to_html_table(get_rank(dmg_etc_df, '지사수수료'), '지사수수료', 'fee_dmg_etc')}</div>
            </div>
        </div>
    </div>
    
    <hr>
    <div style="color:#FFF; font-weight:700; font-size:1.5rem; border-left:5px solid #D4AF37; padding-left:10px; margin-bottom:5px;">👑 부문별 지사수수료 기여 Top 5 FC</div>
    <p style="color:#94A3B8; margin-bottom:20px;">각 부문에서 지사수수료를 가장 많이 창출한 FC 상위 5명입니다. <b style="color:#D4AF37;">이름을 클릭</b>하면 계약 상세내역이 팝업으로 표시됩니다.</p>
    <div class="grid-5">
        {to_top5_html('🔵 생명 익월 수수료', '#3B82F6', life_new_df, 'fee_life_new')}
        {to_top5_html('🟢 생명 유지', '#10B981', life_ret_df, 'fee_life_ret')}
        {to_top5_html('🟠 손해 익월', '#F59E0B', dmg_new_df, 'fee_dmg_new')}
        {to_top5_html('🟣 손해 유지', '#8B5CF6', dmg_ret_df, 'fee_dmg_ret')}
        {to_top5_html('⚪ 손해 기타', '#94A3B8', dmg_gen_only_df, 'fee_dmg_gen')}
    </div>
    
    <div style="text-align:center; color:#334155; font-size:0.8rem; margin-top:4rem; padding:2rem; border-top:1px solid rgba(255,255,255,0.04);">
        웰스FA 수수료 정밀분석 대시보드 HTML Export · Powered by Antigravity
    </div>
</div>

<!-- Modal Background -->
<div id="modalOverlay">
    <div id="modalContent">
        <div class="modal-header">
            <div>
                <span id="modalTitle" style="color:#D4AF37; font-weight:900; font-size:1.5rem;">👤 </span>
                <span id="modalSubtitle" style="color:#64748B; font-size:1rem; margin-left:10px;"></span>
            </div>
            <button class="modal-close" onclick="closeModal()">×</button>
        </div>
        <div class="modal-body">
            <div style="display:flex; gap:20px; margin-bottom:20px;">
                <div class="metric-box"><h3 style="color:#A0AEC0; margin:0 0 10px 0;">📋 계약건수</h3><h2 id="modalCount" style="color:#FFF; margin:0;">0건</h2></div>
                <div class="metric-box"><h3 style="color:#A0AEC0; margin:0 0 10px 0;">💰 수수료 합계</h3><h2 id="modalSum" style="color:#D4AF37; margin:0;">0만원</h2></div>
            </div>
            <div style="max-height: 500px; overflow-y: auto;">
                <table id="modalTable">
                    <thead><tr id="modalThead"></tr></thead>
                    <tbody id="modalTbody"></tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
    const df = {json_data};
    
    const SCOPE_CONDITIONS = {{
        'ach_life_h':  (r) => r['보험군'] === '생명보험' && r['계약일자'].startsWith('202601'),
        'ach_life_p':  (r) => r['보험군'] === '생명보험' && r['계약일자'].startsWith('202601'),
        'ach_dmg_new': (r) => r['보험군'] === '손해보험' && r['계약일자'].startsWith('202601') && r['지급구분'].includes('신계약'),
        'ach_dmg_gen': (r) => r['보험군'] === '손해보험' && r['계약일자'].startsWith('202601') && r['지급구분'].includes('일반'),
        'ach_dmg_car': (r) => r['보험군'] === '손해보험' && r['계약일자'].startsWith('202601') && r['지급구분'].includes('자동차'),
        
        'fee_life_new':(r) => r['보험군'] === '생명보험' && r['지급구분'].includes('신계약'),
        'fee_life_ret':(r) => r['보험군'] === '생명보험' && !r['지급구분'].includes('신계약'),
        'fee_dmg_new': (r) => r['보험군'] === '손해보험' && r['지급구분'].includes('신계약'),
        'fee_dmg_ret': (r) => r['보험군'] === '손해보험' && r['지급구분'].includes('유지'),
        'fee_dmg_etc': (r) => r['보험군'] === '손해보험' && r['지급구분'].match(/일반|자동차|환수/),
        'fee_dmg_gen': (r) => r['보험군'] === '손해보험' && r['지급구분'].includes('일반')
    }};

    const SCOPE_LABELS = {{
        'ach_life_h': '🔵 생명 신계약(환산)', 'ach_life_p': '🔵 생명 신계약(보험료)', 'ach_dmg_new': '🟠 손해 신계약', 'ach_dmg_gen': '⚪ 손해 일반', 'ach_dmg_car': '⚪ 손해 자동차',
        'fee_life_new': '🔵 생명 익월 수수료', 'fee_life_ret': '🟢 생명 유지', 'fee_dmg_new': '🟠 손해 익월', 'fee_dmg_ret': '🟣 손해 유지', 'fee_dmg_etc': '⚪ 손해 기타', 'fee_dmg_gen': '⚪ 손해 일반'
    }};

    function formatNumber(num) {{ return Math.round(num).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ","); }}

    function openCompModal(scope) {{ openDetailModal(scope, null, null); }}

    function openDetailModal(scope, comp, fc) {{
        let filtered = df.filter(SCOPE_CONDITIONS[scope]);
        if(comp) filtered = filtered.filter(r => r['제휴사명'] === comp);
        if(fc)   filtered = filtered.filter(r => r['FC명'] === fc);

        const lblScope = SCOPE_LABELS[scope] || "";
        let mainTitle = fc ? `👤 ${{fc}}` : (comp ? `🏢 ${{comp}}` : `📊 전체 상세`);
        document.getElementById('modalTitle').innerText = mainTitle;
        document.getElementById('modalSubtitle').innerText = `— ${{lblScope}} 부문`;

        const isLife = lblScope.includes('생명');
        const isAch = scope.startsWith('ach_');
        
        // 컬럼 동적 구성
        let cols = ['계약일자', '제휴사명', 'FC명', '지급구분', '상품군', '상품명', '계약자'];
        if(isLife) cols.push('업적지표1', '업적지표2');
        else cols.push('업적지표3');
        if(!isAch) cols.push('지사수수료');

        const headers = cols.map(c => {{
            if(c === '업적지표1') return '환산';
            if(c === '업적지표2') return '생명_보험료';
            if(c === '업적지표3') return '손해_보험료';
            if(c === '지사수수료') return '지사수수료(원)';
            return c;
        }});

        let theadHtml = headers.map(h => `<th>${{h}}</th>`).join('');
        document.getElementById('modalThead').innerHTML = theadHtml;

        let tbodyHtml = '';
        let sumFee = 0;
        filtered.forEach(r => {{
            sumFee += (r['지사수수료'] || 0);
            tbodyHtml += '<tr>';
            cols.forEach(c => {{
                let val = r[c];
                let align = 'center', color = '';
                if(typeof val === 'number') {{
                    align = 'right';
                    if(val < 0) color = 'color:#E63946;';
                    val = formatNumber(val);
                }}
                tbodyHtml += `<td style="text-align:${{align}}; ${{color}}">${{val}}</td>`;
            }});
            tbodyHtml += '</tr>';
        }});
        document.getElementById('modalTbody').innerHTML = tbodyHtml;

        document.getElementById('modalCount').innerText = `${{filtered.length}}건`;
        document.getElementById('modalSum').innerText = `${{formatNumber(sumFee / 10000)}}만원`;

        document.getElementById('modalOverlay').style.display = 'flex';
    }}

    function closeModal() {{
        document.getElementById('modalOverlay').style.display = 'none';
    }}

    // ESC to close
    document.addEventListener('keydown', e => {{
        if(e.key === 'Escape') closeModal();
    }});
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ index.html 파일이 성공적으로 생성되었습니다!")
