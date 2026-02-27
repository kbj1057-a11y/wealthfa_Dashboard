"""
웰스FA · 별자리 네트워크 → 독립형 HTML 생성기
실행하면 브라우저에서 바로 열 수 있는 단일 HTML 파일이 생성됩니다.
"""
import math
import pandas as pd
import json, os, sys, datetime

sys.stdout.reconfigure(encoding='utf-8')

# ── 경로
BASE     = os.path.dirname(os.path.abspath(__file__))
EXCEL    = os.path.join(BASE, "..", "매일업데이트", "26년종합.xlsx")
OUT_HTML = os.path.join(BASE, "..", "매일업데이트", "constellation_network.html")

LIFE_KW = ["생명", "생보", "라이프"]

# ══════════════════════════════════════════════════════
# 1. 데이터 로드
# ══════════════════════════════════════════════════════
def load():
    xl    = pd.ExcelFile(EXCEL)
    sheet = "RAWDATA" if "RAWDATA" in xl.sheet_names else xl.sheet_names[0]
    raw   = pd.read_excel(EXCEL, sheet_name=sheet, engine='openpyxl')

    df = pd.DataFrame()
    df['FC명']    = raw.iloc[:, 2]
    df['제휴사']  = raw.iloc[:, 3]
    df['보험료']  = pd.to_numeric(raw.iloc[:, 8].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    df['환산']    = pd.to_numeric(raw.iloc[:, 9].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    df['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
    p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    df['월P'] = p1 + p2
    df = df[df['FC명'].notna()].copy()

    def is_life(c): return any(kw in str(c) for kw in LIFE_KW) if pd.notna(c) else False
    df['is_life'] = df['제휴사'].apply(is_life)
    df['year']    = df['계약일자'].dt.year
    df['month']   = df['계약일자'].dt.month

    # 2026년 2월 데이터만
    df_2602 = df[(df['year'] == 2026) & (df['month'] == 2)]

    fc_stats = []
    for fc in df['FC명'].unique():
        fc_curr = df_2602[df_2602['FC명'] == fc]
        cumP    = fc_curr['월P'].sum()
        cnt     = len(fc_curr)
        fc_stats.append({'FC명': fc, '월P': cumP, '건수': cnt})

    fc_df = pd.DataFrame(fc_stats).sort_values('월P', ascending=False)
    max_P = fc_df['월P'].max() or 1

    # 지표
    life_df    = df_2602[df_2602['is_life'] == True]
    nonlife_df = df_2602[df_2602['is_life'] == False]

    return {
        'fc_df':        fc_df,
        'max_P':        max_P,
        'active_fc':    int((fc_df['건수'] > 0).sum()),
        'life_hwan':    int(life_df['환산'].sum()),
        'life_prem':    int(life_df['보험료'].sum()),
        'nonlife_prem': int(nonlife_df['보험료'].sum()),
        'top3_p':       fc_df.nlargest(3, '월P')[['FC명','월P']].values.tolist(),
        'top3_cnt':     fc_df.nlargest(3, '건수')[['FC명','건수']].values.tolist(),
    }

# ══════════════════════════════════════════════════════
# 2. ECharts 옵션 빌드
# ══════════════════════════════════════════════════════
def build_echarts_option(fc_df, max_P):
    nodes, links = [], []

    # 중심 노드 (웰스FA)
    nodes.append({
        "id": "CENTER", "name": "웰스FA",
        "symbolSize": 56,
        "value": "웰스FA",
        "fixed": True, "x": 0, "y": 0,
        "label": {"show": True, "fontSize": 13, "fontWeight": "bold", "color": "#FFFFFF"},
        "itemStyle": {
            "color": "#FFFFFF",
            "shadowBlur": 80, "shadowColor": "rgba(255,255,255,0.95)",
            "borderColor": "rgba(255,255,255,0.5)", "borderWidth": 2
        }
    })

    n_fc = len(fc_df)
    for idx, (_, row) in enumerate(fc_df.iterrows()):
        fc    = row['FC명']
        val   = float(row['월P'])
        # 원형 초기 배치 - 모든 FC를 360도 등간격으로 배치
        angle  = (2 * math.pi * idx) / max(n_fc, 1)
        radius = 280  # 중심으로부터의 초기 거리
        init_x = round(radius * math.cos(angle), 1)
        init_y = round(radius * math.sin(angle), 1)
        ratio = val / float(max_P)
        size  = 12 + ratio * 40
        glow  = 18 + ratio * 58
        r     = int(180 + ratio * 75)
        g     = int(120 + ratio * 90)
        b     = 0
        color = f"rgb({r},{g},{b})"
        glow_c= f"rgba({r},{g},{b},0.88)"

        nodes.append({
            "id": fc, "name": fc,
            "symbolSize": round(size, 1),
            "value": int(val),
            "x": init_x, "y": init_y,   # 원형 초기 배치
            "label": {
                "show": True,
                "fontSize": max(8, round(8 + ratio * 4)),
                "color": color,
                "textShadowBlur": 8, "textShadowColor": glow_c
            },
            "itemStyle": {
                "color": color,
                "shadowBlur": round(glow),
                "shadowColor": glow_c,
                "borderColor": color, "borderWidth": 1,
                "opacity": round(0.50 + ratio * 0.50, 2)
            }
        })

        alpha_line = round(0.06 + ratio * 0.22, 2)
        links.append({
            "source": "CENTER", "target": fc,
            "lineStyle": {
                "color": f"rgba(212,175,55,{alpha_line})",
                "width": max(0.5, round(ratio * 2, 1)),
                "curveness": 0.28
            }
        })

    option = {
        "backgroundColor": "#000000",
        "tooltip": {
            "show": True,
            "backgroundColor": "rgba(0,0,0,0.9)",
            "borderColor": "rgba(212,175,55,0.4)",
            "textStyle": {"color": "#FFD700", "fontSize": 13},
            "formatter": "{b}<br/>2월 월P: {c}원"
        },
        "animationDuration": 2500,
        "animationEasingUpdate": "quinticInOut",
        "series": [{
            "type": "graph",
            "layout": "force",
            "data": nodes,
            "links": links,
            "roam": True,
            "draggable": True,
            "force": {
                "repulsion": [200, 380],   # 더 강하게 밀어내서 고르게 퍼짐
                "gravity": 0.04,           # 약한 중심 인력
                "edgeLength": [100, 280],  # 링크 길이 범위
                "friction": 0.5,
                "layoutAnimation": True
            },
            "label": {"position": "bottom", "distance": 4},
            "emphasis": {
                "focus": "adjacency",
                "lineStyle": {"width": 3},
                "itemStyle": {"shadowBlur": 100}
            }
        }]
    }
    return option

# ══════════════════════════════════════════════════════
# 3. HTML 생성
# ══════════════════════════════════════════════════════
def fmt_man(v):
    return f"{int(v/10000):,}만원" if v >= 10000 else f"{int(v):,}원"

def build_html(data, option_json, now_str):
    top3_p_html   = "".join([f'<div class="top-row"><span>#{i+1}</span>{r[0]} &nbsp; {fmt_man(r[1])}</div>' for i, r in enumerate(data['top3_p'])])
    top3_cnt_html = "".join([f'<div class="top-row"><span>#{i+1}</span>{r[0]} &nbsp; {int(r[1])}건</div>'   for i, r in enumerate(data['top3_cnt'])])

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WEALTH FA · 2026년 2월 · Constellation Network</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300;400;700&family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#000; color:#fff; font-family:'Noto Sans KR','Montserrat',sans-serif; height:100vh; overflow:hidden; }}

/* 헤더 */
.header {{
    text-align:center; padding:14px 0 8px;
    border-bottom:1px solid rgba(212,175,55,0.2);
}}
.main-title {{
    font-family:'Montserrat',sans-serif; font-weight:300;
    font-size:1.1rem; letter-spacing:0.5em;
    color:rgba(212,175,55,0.88); text-transform:uppercase;
}}
.main-sub {{
    font-size:0.58rem; color:rgba(255,255,255,0.25);
    letter-spacing:0.3em; margin-top:3px;
}}

/* 메트릭 바 */
.metrics {{
    display:grid; grid-template-columns: 1fr 1.2fr 1.2fr 1.2fr 1.6fr 1.6fr;
    gap:8px; padding:8px 16px;
}}
.card {{
    background:linear-gradient(135deg,rgba(212,175,55,0.07),rgba(0,0,0,0.95));
    border:1px solid rgba(212,175,55,0.22); border-radius:10px;
    padding:8px 12px; text-align:center;
}}
.card-title {{
    font-size:0.55rem; color:rgba(212,175,55,0.65);
    letter-spacing:0.12em; text-transform:uppercase;
    font-family:'Montserrat',sans-serif; margin-bottom:4px;
}}
.card-val {{
    font-size:1.25rem; font-weight:700; color:#D4AF37;
    text-shadow:0 0 15px rgba(212,175,55,0.55);
}}
.top-card {{ text-align:left; }}
.top-row {{
    font-size:0.72rem; color:rgba(255,255,255,0.82);
    padding:1px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.top-row span {{ color:#D4AF37; font-weight:700; margin-right:4px; }}

/* 차트 */
#chart {{ width:100%; height:calc(100vh - 185px); }}

/* 하단 */
.footer {{
    text-align:center; padding:4px;
    font-size:0.55rem; color:rgba(255,255,255,0.18);
    letter-spacing:0.2em;
}}

/* 별 파티클 배경 효과 */
@keyframes twinkle {{
    0%,100% {{ opacity:0.2; }} 50% {{ opacity:0.8; }}
}}
</style>
</head>
<body>

<div class="header">
    <div class="main-title">✦ &nbsp; WEALTH FA &nbsp; 2026년 2월 &nbsp; ✦</div>
    <div class="main-sub">{now_str} &nbsp;·&nbsp; LIVE PERFORMANCE CONSTELLATION</div>
</div>

<div class="metrics">
    <div class="card">
        <div class="card-title">ACTIVE FC</div>
        <div class="card-val">{data['active_fc']}명</div>
    </div>
    <div class="card">
        <div class="card-title">생명 환산</div>
        <div class="card-val">{fmt_man(data['life_hwan'])}</div>
    </div>
    <div class="card">
        <div class="card-title">생명 보험료</div>
        <div class="card-val">{fmt_man(data['life_prem'])}</div>
    </div>
    <div class="card">
        <div class="card-title">손해 보험료</div>
        <div class="card-val">{fmt_man(data['nonlife_prem'])}</div>
    </div>
    <div class="card top-card">
        <div class="card-title">TOP 3 · 월P 실적</div>
        {top3_p_html}
    </div>
    <div class="card top-card">
        <div class="card-title">TOP 3 · 계약 건수</div>
        {top3_cnt_html}
    </div>
</div>

<div id="chart"></div>

<div class="footer">
    ◈ &nbsp; 별의 크기 = 2월 누적 월P (익월수수료 + 익월시책) &nbsp;·&nbsp; 밝을수록 실적 높음 &nbsp;·&nbsp; 드래그·줌 가능
</div>

<script>
var chart = echarts.init(document.getElementById('chart'), null, {{renderer: 'canvas'}});
var option = {option_json};
chart.setOption(option);
window.addEventListener('resize', function() {{ chart.resize(); }});
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════
# 4. 실행
# ══════════════════════════════════════════════════════
def main():
    print("데이터 로드 중...")
    data   = load()
    option = build_echarts_option(data['fc_df'], data['max_P'])
    now_str = datetime.datetime.now().strftime("%Y.%m.%d %H:%M")

    option_json = json.dumps(option, ensure_ascii=False, indent=2)
    html = build_html(data, option_json, now_str)

    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"SUCCESS: {OUT_HTML}")
    print(f"FC {len(data['fc_df'])}명 / 가동 {data['active_fc']}명")

if __name__ == "__main__":
    main()
