"""
╔══════════════════════════════════════════════════════════════╗
║   웰스FA · 별자리 네트워크 (Constellation Network)           ║
║   VVIP 라운지급 지점 메인 TV 전용 실적 시각화                 ║
╚══════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import pandas as pd
import os, datetime, time
from streamlit_echarts import st_echarts

# ── 페이지 전체 설정 ────────────────────────────────────────
st.set_page_config(
    page_title="WEALTH FA 2026",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── 전역 CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300;400;700&family=Noto+Sans+KR:wght@300;400;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #000000 !important;
    color: #ffffff;
    font-family: 'Noto Sans KR', 'Montserrat', sans-serif;
}
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
.block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
header[data-testid="stHeader"] { background: transparent; height: 0; }
[data-testid="stSidebar"] { display: none; }
footer { display: none; }
[data-testid="stStatusWidget"] { display: none; }

/* 메트릭 카드 */
.metric-card {
    background: linear-gradient(135deg, rgba(212,175,55,0.07), rgba(0,0,0,0.95));
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 10px;
    padding: 10px 14px;
    text-align: center;
    height: 100%;
}
.metric-title {
    font-size: 0.58rem;
    color: rgba(212,175,55,0.65);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 5px;
    font-family: 'Montserrat', sans-serif;
}
.metric-value {
    font-size: 1.35rem;
    font-weight: 700;
    color: #D4AF37;
    text-shadow: 0 0 18px rgba(212,175,55,0.55);
}
.metric-sub {
    font-size: 0.6rem;
    color: rgba(255,255,255,0.3);
    margin-top: 1px;
}

/* TOP 카드 */
.top-card {
    background: linear-gradient(135deg, rgba(212,175,55,0.07), rgba(0,0,0,0.95));
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 10px;
    padding: 10px 14px;
    text-align: left;
}
.top-title {
    font-size: 0.6rem;
    color: rgba(212,175,55,0.65);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Montserrat', sans-serif;
}
.top-row {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.85);
    padding: 1px 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.top-row span {
    color: #D4AF37;
    font-weight: 700;
    margin-right: 4px;
}

/* 타이틀 */
.main-title {
    font-family: 'Montserrat', sans-serif;
    font-weight: 300;
    font-size: 1.15rem;
    letter-spacing: 0.5em;
    color: rgba(212,175,55,0.85);
    text-align: center;
    text-transform: uppercase;
}
.main-subtitle {
    font-size: 0.6rem;
    color: rgba(255,255,255,0.25);
    text-align: center;
    letter-spacing: 0.3em;
    text-transform: uppercase;
}
iframe { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 1. 데이터 로드 & 가공
# ══════════════════════════════════════════════════════════════
LIFE_KW = ["생명", "생보", "라이프"]

@st.cache_data(ttl=300)
def load_data():
    candidates = [
        r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년종합.xlsx",
        os.path.join(os.path.dirname(__file__), "..", "매일업데이트", "26년종합.xlsx"),
        "매일업데이트/26년종합.xlsx",
    ]
    path = next((p for p in candidates if os.path.exists(p)), None)
    if not path:
        return None

    xl    = pd.ExcelFile(path)
    sheet = "RAWDATA" if "RAWDATA" in xl.sheet_names else xl.sheet_names[0]
    raw   = pd.read_excel(path, sheet_name=sheet, engine='openpyxl')

    df = pd.DataFrame()
    df['FC명']    = raw.iloc[:, 2]   # FC명
    df['제휴사']  = raw.iloc[:, 3]   # 제휴사 (생명/손해 구분용)
    df['보험료']  = pd.to_numeric(raw.iloc[:, 8].astype(str).str.replace(',',''), errors='coerce').fillna(0)   # 보험료
    df['환산']    = pd.to_numeric(raw.iloc[:, 9].astype(str).str.replace(',',''), errors='coerce').fillna(0)   # 환산_1회
    df['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
    p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)  # 익월수수료
    p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)  # 익월시책
    df['월P'] = p1 + p2

    df = df[df['FC명'].notna()].copy()

    # 생명/손해 구분
    def is_life(c):
        return any(kw in str(c) for kw in LIFE_KW) if pd.notna(c) else False
    df['is_life'] = df['제휴사'].apply(is_life)

    # 2026년 2월 데이터만 필터
    df['year']  = df['계약일자'].dt.year
    df['month'] = df['계약일자'].dt.month
    df_2602 = df[(df['year'] == 2026) & (df['month'] == 2)].copy()

    # FC별 집계 (월P 기준 - 전체 데이터)
    fc_stats = []
    all_fcs = df['FC명'].unique()
    for fc in all_fcs:
        fc_curr = df_2602[df_2602['FC명'] == fc]
        # 월P와 건수 모두 2026년 2월 데이터만 기준
        cumP = fc_curr['월P'].sum()
        cnt  = len(fc_curr)
        fc_stats.append({
            'FC명':   fc,
            '누적월P': cumP,
            '건수':    cnt,
        })

    fc_df = pd.DataFrame(fc_stats)

    # 지표 계산
    # 가동숫자: 2월에 계약이 1건 이상인 FC
    active_fc = int((fc_df['건수'] > 0).sum())

    # 생명보험 환산 (2월)
    life_df    = df_2602[df_2602['is_life'] == True]
    nonlife_df = df_2602[df_2602['is_life'] == False]

    life_hwan  = int(life_df['환산'].sum())
    life_prem  = int(life_df['보험료'].sum())
    nonlife_prem = int(nonlife_df['보험료'].sum())

    return {
        'fc_df':        fc_df.sort_values('누적월P', ascending=False),
        'active_fc':    active_fc,
        'life_hwan':    life_hwan,
        'life_prem':    life_prem,
        'nonlife_prem': nonlife_prem,
    }


# ══════════════════════════════════════════════════════════════
# 2. ECharts 그래프 옵션 빌더
# ══════════════════════════════════════════════════════════════
def build_option(fc_df):
    max_P = fc_df['누적월P'].max() if not fc_df.empty else 1

    # ── 노드 구성
    nodes = []

    # 중심: 지점장
    nodes.append({
        "id": "CENTER",
        "name": "지점장",
        "symbolSize": 55,
        "value": 0,
        "label":{"show": True, "fontSize": 13, "fontWeight": "bold", "color": "#FFFFFF"},
        "itemStyle":{
            "color": "#FFFFFF",
            "shadowBlur": 70, "shadowColor": "rgba(255,255,255,0.9)",
            "borderColor": "rgba(255,255,255,0.5)", "borderWidth": 2,
        },
        "fixed": True, "x": 0, "y": 0,
        "category": 0,
    })

    # FC 노드 — 단일 카테고리(골드), 크기만 다름
    for _, row in fc_df.iterrows():
        fc   = row['FC명']
        val  = row['누적월P']
        ratio = val / max(max_P, 1)

        # 크기: 최소 12 ~ 최대 50
        size  = 12 + ratio * 38
        # 발광: 실적 클수록 더 밝게
        glow  = 20 + ratio * 55
        # 투명도: 실적 클수록 더 선명
        alpha = 0.5 + ratio * 0.5
        # 색상: 실적에 따라 골드 농도 변화 (낮으면 흐린 골드, 높으면 선명한 골드)
        r = int(180 + ratio * 75)
        g = int(130 + ratio * 85)
        b = int(0)
        color = f"rgb({r},{g},{b})"
        glow_color = f"rgba({r},{g},{b},0.85)"

        nodes.append({
            "id": fc, "name": fc,
            "category": 1,
            "symbolSize": round(size, 1),
            "value": int(val),
            "label":{
                "show": True,
                "fontSize": max(8, round(8 + ratio * 4)),
                "color": color,
                "textShadowBlur": 10,
                "textShadowColor": glow_color,
            },
            "itemStyle":{
                "color": color,
                "shadowBlur": round(glow),
                "shadowColor": glow_color,
                "borderColor": color,
                "borderWidth": 1,
                "opacity": alpha,
            },
        })

    # ── 링크: 지점장 → 모든 FC (방사형)
    links = []
    for _, row in fc_df.iterrows():
        fc    = row['FC명']
        ratio = row['누적월P'] / max(max_P, 1)
        alpha = round(0.08 + ratio * 0.22, 2)
        links.append({
            "source": "CENTER",
            "target": fc,
            "lineStyle":{
                "color": f"rgba(212,175,55,{alpha})",
                "width": max(0.5, ratio * 2),
                "curveness": 0.25,
                "shadowBlur": 3,
                "shadowColor": "rgba(212,175,55,0.1)",
            }
        })

    categories = [
        {"name": "지점장"},
        {"name": "FC",  "itemStyle": {"color": "#D4AF37"}},
    ]

    return {
        "backgroundColor": "#000000",
        "tooltip":{
            "show": True,
            "backgroundColor": "rgba(0,0,0,0.88)",
            "borderColor": "rgba(212,175,55,0.35)",
            "borderWidth": 1,
            "textStyle": {"color": "#FFD700", "fontSize": 12},
            "formatter": "{b}<br/>누적 월P: {c}원",
        },
        "animationDuration": 2000,
        "animationEasingUpdate": "quinticInOut",
        "series":[{
            "type": "graph",
            "layout": "force",
            "data": nodes,
            "links": links,
            "categories": categories,
            "roam": True,
            "draggable": True,
            "force":{
                "repulsion": [150, 280],
                "gravity": 0.05,
                "edgeLength": [90, 240],
                "friction": 0.55,
                "layoutAnimation": True,
            },
            "label":{"position": "bottom", "distance": 5, "fontFamily": "Noto Sans KR, sans-serif"},
            "emphasis":{
                "focus": "adjacency",
                "lineStyle": {"width": 3},
                "itemStyle": {"shadowBlur": 90},
            },
        }]
    }


# ══════════════════════════════════════════════════════════════
# 3. 메인 렌더링
# ══════════════════════════════════════════════════════════════
def fmt_man(v):
    """만원 단위 포맷"""
    return f"{int(v/10000):,}만" if v >= 10000 else f"{int(v):,}"

def main():
    data = load_data()
    now  = datetime.datetime.now()

    # ── 타이틀
    st.markdown(f"""
    <div style="padding:10px 0 8px; border-bottom:1px solid rgba(212,175,55,0.18); margin-bottom:10px;">
        <div class="main-title">✦ &nbsp; WEALTH FA &nbsp; 2026년 2월 &nbsp; ✦</div>
        <div class="main-subtitle" style="margin-top:4px;">{now.strftime('%Y.%m.%d  %H:%M')} &nbsp;·&nbsp; LIVE PERFORMANCE CONSTELLATION</div>
    </div>
    """, unsafe_allow_html=True)

    if not data:
        st.error("📂 데이터를 찾을 수 없습니다.")
        return

    fc_df        = data['fc_df']
    active_fc    = data['active_fc']
    life_hwan    = data['life_hwan']
    life_prem    = data['life_prem']
    nonlife_prem = data['nonlife_prem']

    # TOP3 by 월P
    top3_p   = fc_df.nlargest(3, '누적월P')[['FC명', '누적월P']]
    # TOP3 by 건수 (2월)
    top3_cnt = fc_df.nlargest(3, '건수')[['FC명', '건수']]

    # ── 메트릭 바 (6칸)
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1.2, 1.2, 1.2, 1.5, 1.5])

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ACTIVE FC</div>
            <div class="metric-value">{active_fc}명</div>
            <div class="metric-sub">가동 FC</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">생명 환산</div>
            <div class="metric-value">{fmt_man(life_hwan)}</div>
            <div class="metric-sub">생명보험 환산보험료</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">생명 보험료</div>
            <div class="metric-value">{fmt_man(life_prem)}</div>
            <div class="metric-sub">생명보험 보험료</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">손해 보험료</div>
            <div class="metric-value">{fmt_man(nonlife_prem)}</div>
            <div class="metric-sub">손해보험 보험료</div>
        </div>""", unsafe_allow_html=True)

    # TOP3 by 월P
    with c5:
        rows_p = "".join([
            f'<div class="top-row"><span>#{i+1}</span>{row["FC명"]} &nbsp; {fmt_man(row["누적월P"])}</div>'
            for i, (_, row) in enumerate(top3_p.iterrows())
        ])
        st.markdown(f"""
        <div class="top-card">
            <div class="top-title">TOP 3 · 월P 실적</div>
            {rows_p}
        </div>""", unsafe_allow_html=True)

    # TOP3 by 건수
    with c6:
        rows_c = "".join([
            f'<div class="top-row"><span>#{i+1}</span>{row["FC명"]} &nbsp; {int(row["건수"])}건</div>'
            for i, (_, row) in enumerate(top3_cnt.iterrows())
        ])
        st.markdown(f"""
        <div class="top-card">
            <div class="top-title">TOP 3 · 계약 건수</div>
            {rows_c}
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── 별자리 네트워크
    option = build_option(fc_df)
    st_echarts(options=option, height="76vh", key="constellation")

    # ── 하단 범례
    st.markdown("""
    <div style="text-align:center; margin-top:4px; font-size:0.6rem;
                color:rgba(255,255,255,0.2); letter-spacing:0.2em;">
        ◈ &nbsp; 별의 크기 = 누적 월P (익월수수료 + 익월시책) &nbsp;·&nbsp;
        밝을수록 실적 높음 &nbsp;·&nbsp; 드래그·줌 가능
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
