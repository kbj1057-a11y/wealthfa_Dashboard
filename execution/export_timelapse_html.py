"""
웰스FA · 별자리 타임랩스 HTML
레이아웃: 좌3카드 | 중앙 애니메이션 | 우3카드
TOP7 / 월P 구간 표시
"""
import math, json, os, sys, datetime
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE     = os.path.dirname(os.path.abspath(__file__))
EXCEL    = os.path.join(BASE, "..", "매일업데이트", "26년종합.xlsx")
OUT_HTML = os.path.join(BASE, "..", "매일업데이트", "constellation_timelapse.html")
START    = datetime.date(2026, 2, 1)
END      = datetime.date.today()
LIFE_KW  = ["생명", "생보", "라이프"]

# ── 월P 구간 레이블 (100만 단위 절사)
def p_tier(v):
    wan = v / 10000          # 원 → 만원 변환
    if wan <= 0: return "실적 없음"
    floored = int(wan // 100) * 100  # 100만 단위 내림 (1392→1300, 467→400)
    return f"{floored:,}만 이상"

def fmt_man(v):
    return f"{int(v/10000):,}만" if v >= 10000 else (f"{int(v):,}" if v > 0 else "-")

# ══════════════════════════════════════════════════
# 1. 데이터 로드
# ══════════════════════════════════════════════════
def load():
    excel_time = datetime.datetime.fromtimestamp(
        os.path.getmtime(EXCEL)).strftime("%Y.%m.%d  %H:%M")

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
    df['날짜']  = df['계약일자'].dt.date
    df['year']  = df['계약일자'].dt.year
    df['month'] = df['계약일자'].dt.month

    df_2602 = df[(df['year'] == 2026) & (df['month'] == 2)]

    life_df    = df_2602[df_2602['is_life'] == True]
    nonlife_df = df_2602[df_2602['is_life'] == False]

    fc_stats = []
    for fc in df['FC명'].unique():
        fc_curr = df_2602[df_2602['FC명'] == fc]
        fc_stats.append({'FC명': fc, '월P': fc_curr['월P'].sum(), '건수': len(fc_curr)})
    fc_df = pd.DataFrame(fc_stats).sort_values('월P', ascending=False)

    top7_p   = fc_df.nlargest(7, '월P')[['FC명','월P']].values.tolist()
    top7_cnt = fc_df.nlargest(7, '건수')[['FC명','건수']].values.tolist()

    metrics = {
        'excel_time':   excel_time,
        'active_fc':    int((fc_df['건수'] > 0).sum()),
        'life_hwan':    int(life_df['환산'].sum()),
        'life_prem':    int(life_df['보험료'].sum()),
        'nonlife_prem': int(nonlife_df['보험료'].sum()),
        'top7_p':       top7_p,
        'top7_cnt':     top7_cnt,
        # 피날레 시퀀스용 FC명 순서 리스트
        'top7_p_names': [r[0] for r in top7_p],
    }

    # 타임랩스 데이터
    df_anim   = df[(df['날짜'] >= START) & (df['날짜'] <= END)]
    all_dates = sorted({START + datetime.timedelta(days=i) for i in range((END-START).days+1)})
    all_fcs   = sorted(df_anim['FC명'].unique().tolist())

    daily = df_anim.groupby(['FC명','날짜'])['월P'].sum().unstack(fill_value=0)
    for d in all_dates:
        if d not in daily.columns: daily[d] = 0
    daily     = daily.reindex(columns=sorted(daily.columns))
    cumul     = daily.cumsum(axis=1)
    global_max = cumul.max().max() or 1

    return all_fcs, all_dates, cumul, global_max, metrics

# ══════════════════════════════════════════════════
# 2. ECharts 데이터 빌드
# ══════════════════════════════════════════════════
def circle_positions(n, radius=300):
    return [(round(radius*math.cos(2*math.pi*i/max(n,1)),1),
             round(radius*math.sin(2*math.pi*i/max(n,1)),1)) for i in range(n)]

def ncolor(r): return f"rgb({int(180+r*75)},{int(120+r*90)},0)"
def gcolor(r): return f"rgba({int(180+r*75)},{int(120+r*90)},0,0.88)"

def build_echarts(all_fcs, all_dates, cumul, global_max):
    n_fc = len(all_fcs)
    pos  = circle_positions(n_fc)

    init_nodes = [{"id":"CENTER","name":"웰스FA","symbolSize":54,"value":"웰스FA",
                   "fixed":True,"x":0,"y":0,
                   "label":{"show":True,"fontSize":22,"fontWeight":"bold","color":"#FFFFFF",
                             "textShadowBlur":12,"textShadowColor":"rgba(255,255,255,0.8)"},
                   "itemStyle":{"color":"#FFFFFF","shadowBlur":75,
                                "shadowColor":"rgba(255,255,255,0.9)",
                                "borderColor":"rgba(255,255,255,0.4)","borderWidth":2}}]
    for i, fc in enumerate(all_fcs):
        x,y = pos[i]
        init_nodes.append({"id":fc,"name":fc,"symbolSize":10,"value":0,
                           "x":float(x),"y":float(y),
                           "label":{"show":True,"fontSize":14,"color":"rgb(180,120,0)",
                                    "textShadowBlur":4,"textShadowColor":"rgba(180,120,0,0.4)"},
                           "itemStyle":{"color":"rgb(180,120,0)","shadowBlur":10,
                                        "shadowColor":"rgba(180,120,0,0.4)",
                                        "borderColor":"rgb(180,120,0)","borderWidth":1,"opacity":0.35}})

    init_links = [{"source":"CENTER","target":fc,
                   "lineStyle":{"color":"rgba(212,175,55,0.05)","width":0.5,"curveness":0.28}}
                  for fc in all_fcs]

    init_option = {"backgroundColor":"#000000",
                   "tooltip":{"show":True,"backgroundColor":"rgba(0,0,0,0.9)",
                              "borderColor":"rgba(212,175,55,0.4)",
                              "textStyle":{"color":"#FFD700","fontSize":12}},
                   "animationDurationUpdate":600,"animationEasingUpdate":"cubicOut",
                   "series":[{"type":"graph","layout":"force",
                              "data":init_nodes,"links":init_links,
                              "roam":True,"draggable":True,
                              "force":{"repulsion":[200,380],"gravity":0.04,
                                       "edgeLength":[100,280],"friction":0.5,"layoutAnimation":True},
                              "label":{"position":"bottom","distance":4},
                              "emphasis":{"focus":"adjacency","lineStyle":{"width":3}}}]}

    frames_data = []
    for date in all_dates:
        dn, dl = [{"id":"CENTER","name":"웰스FA","symbolSize":54,"value":"웰스FA"}], []
        for fc in all_fcs:
            val   = float(cumul.loc[fc,date]) if fc in cumul.index else 0.0
            ratio = val/float(global_max)
            size  = 10+ratio*44; glow = 12+ratio*62; alpha = round(0.35+ratio*0.65,2)
            # 라벨 폰트: 16(base)~28(max), 실적 없으면 14
            lsize = max(14, round(16 + ratio * 12))
            dn.append({"id":fc,"name":fc,"symbolSize":round(size,1),"value":int(val),
                       "label":{"show":True,"fontSize":lsize,
                                "color":ncolor(ratio),"textShadowBlur":max(6,round(ratio*14)),
                                "textShadowColor":gcolor(ratio),
                                "fontWeight":"bold" if ratio>0.2 else "normal"},
                       "itemStyle":{"color":ncolor(ratio),"shadowBlur":round(glow),
                                    "shadowColor":gcolor(ratio),"borderColor":ncolor(ratio),
                                    "borderWidth":1,"opacity":alpha}})
            a = round(0.05+ratio*0.25,2)
            dl.append({"source":"CENTER","target":fc,
                       "lineStyle":{"color":f"rgba(212,175,55,{a})",
                                    "width":max(0.5,round(ratio*2.5,1)),"curveness":0.28}})
        frames_data.append({"nodes":dn,"links":dl})

    return (json.dumps(init_option, ensure_ascii=False),
            json.dumps(frames_data,  ensure_ascii=False),
            json.dumps([f"{d.month}/{d.day}" for d in all_dates], ensure_ascii=False))

# ══════════════════════════════════════════════════
# 3. HTML
# ══════════════════════════════════════════════════
def build_html(all_fcs, all_dates, cumul, global_max, metrics):
    init_json, frames_json, dates_json = build_echarts(all_fcs, all_dates, cumul, global_max)

    # 피날레 JS용 데이터 직렬화
    top7_names_json = json.dumps(metrics['top7_p_names'], ensure_ascii=False)
    top7_info_json  = json.dumps(
        [{"name": r[0], "tier": p_tier(r[1])} for r in metrics['top7_p']],
        ensure_ascii=False
    )

    def top7_p_rows():
        rows = ""
        for i, r in enumerate(metrics['top7_p']):
            tier = p_tier(r[1])
            rows += f'<div class="top-row"><span>#{i+1}</span><span class="fc-name">{r[0]}</span><span class="tier">{tier}</span></div>'
        return rows

    def top7_cnt_rows():
        rows = ""
        for i, r in enumerate(metrics['top7_cnt']):
            rows += f'<div class="top-row"><span>#{i+1}</span><span class="fc-name">{r[0]}</span><span class="cnt-val">{int(r[1])}건</span></div>'
        return rows

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>WEALTH FA · 2026년 2월 · Constellation</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300;700&family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#000;color:#fff;font-family:'Noto Sans KR','Montserrat',sans-serif;
     height:100vh;overflow:hidden;display:flex;flex-direction:column;}}

/* ── 최상단 헤더 */
.header{{text-align:center;padding:16px 0 10px;
         border-bottom:1px solid rgba(212,175,55,0.18);flex-shrink:0;}}
.main-title{{font-family:'Montserrat',sans-serif;font-weight:300;font-size:2rem;
             letter-spacing:0.5em;color:rgba(212,175,55,0.9);text-transform:uppercase;}}
.update-time{{font-size:1.1rem;color:rgba(212,175,55,0.5);letter-spacing:0.15em;margin-top:5px;}}

/* ── 본문: 좌패널 | 중앙 | 우패널 */
.body-wrap{{flex:1;display:flex;min-height:0;gap:0;}}

/* 좌/우 패널 공통 */
.side-panel{{
    width:340px; flex-shrink:0;
    display:flex; flex-direction:column;
    padding:12px 16px; gap:10px;
    border-right:1px solid rgba(212,175,55,0.1);
    overflow:hidden;
}}
.side-panel.right{{border-right:none;border-left:1px solid rgba(212,175,55,0.1);width:390px;}}

.s-card{{
    background:linear-gradient(135deg,rgba(212,175,55,0.07),rgba(0,0,0,0.95));
    border:1px solid rgba(212,175,55,0.2);border-radius:12px;
    padding:14px 18px;flex-shrink:0;
}}
.s-card.grow{{flex:1;overflow:hidden;display:flex;flex-direction:column;}}
.card-title{{font-size:1.05rem;color:rgba(212,175,55,0.7);letter-spacing:0.1em;
             text-transform:uppercase;font-family:'Montserrat',sans-serif;margin-bottom:8px;}}
.card-val{{font-size:2.5rem;font-weight:700;color:#D4AF37;
           text-shadow:0 0 20px rgba(212,175,55,0.6);}}
.card-sub{{font-size:0.85rem;color:rgba(255,255,255,0.28);margin-top:4px;}}

/* TOP7 행 */
.top-rows{{flex:1;overflow:hidden;display:flex;flex-direction:column;justify-content:space-evenly;gap:3px;}}
.top-row{{
    display:flex;align-items:center;gap:8px;
    font-size:1.25rem;padding:4px 3px;
    border-bottom:1px solid rgba(212,175,55,0.08);
}}
.top-row span{{color:#D4AF37;font-weight:700;font-size:1.1rem;flex-shrink:0;min-width:34px;}}
.fc-name{{color:rgba(255,255,255,0.9);flex:1;
          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:1.25rem;}}
.tier{{color:rgba(212,175,55,0.85);font-size:1.1rem;flex-shrink:0;white-space:nowrap;font-weight:600;}}
.cnt-val{{color:rgba(100,200,255,0.95);font-size:1.15rem;flex-shrink:0;font-weight:600;}}

/* ── 중앙 영역 */
.center-panel{{flex:1;display:flex;flex-direction:column;min-width:0;}}
.date-display{{text-align:center;padding:6px 0 3px;flex-shrink:0;}}
.current-date{{font-family:'Montserrat',sans-serif;font-weight:100;font-size:3.8rem;
               letter-spacing:0.3em;color:rgba(212,175,55,0.88);
               text-shadow:0 0 32px rgba(212,175,55,0.4);transition:all 0.5s ease;}}
.date-label{{font-size:0.85rem;color:rgba(255,255,255,0.22);letter-spacing:0.3em;}}

#chart{{flex:1;min-height:0;}}

.controls{{flex-shrink:0;display:flex;align-items:center;justify-content:center;
           gap:14px;padding:8px 18px 10px;
           border-top:1px solid rgba(212,175,55,0.1);}}
.btn{{background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.3);
      color:#D4AF37;padding:6px 20px;border-radius:20px;cursor:pointer;
      font-size:1rem;font-family:'Montserrat',sans-serif;transition:all 0.2s;}}
.btn:hover{{background:rgba(212,175,55,0.22);}}
.btn.active{{background:rgba(212,175,55,0.28);box-shadow:0 0 15px rgba(212,175,55,0.35);}}
.progress-wrap{{flex:1;max-width:400px;}}
.progress-bg{{height:5px;background:rgba(212,175,55,0.1);border-radius:3px;cursor:pointer;overflow:hidden;}}
.progress-fill{{height:100%;background:linear-gradient(90deg,#D4AF37,#FFD700);width:0%;
                transition:width 0.5s ease;box-shadow:0 0 9px rgba(212,175,55,0.5);border-radius:3px;}}
.speed-label{{font-size:0.85rem;color:rgba(212,175,55,0.4);white-space:nowrap;}}
select.speed-sel{{background:rgba(212,175,55,0.07);border:1px solid rgba(212,175,55,0.2);
                  color:#D4AF37;padding:4px 10px;border-radius:8px;font-size:0.9rem;cursor:pointer;}}

/* ── 랭크 뱃지 오버레이 (피날레용) */
#rankBadge{{
    position:fixed; top:50%; left:50%;
    transform:translate(-50%,-50%) scale(0.6);
    background:radial-gradient(ellipse at center,
        rgba(212,175,55,0.18) 0%, rgba(0,0,0,0.92) 70%);
    border:2px solid rgba(212,175,55,0.5);
    border-radius:20px;
    padding:24px 44px;
    text-align:center;
    pointer-events:none;
    opacity:0;
    transition:all 0.45s cubic-bezier(0.34,1.56,0.64,1);
    z-index:9999;
    box-shadow:0 0 60px rgba(212,175,55,0.25), inset 0 0 40px rgba(212,175,55,0.05);
}}
#rankBadge.show{{
    opacity:1;
    transform:translate(-50%,-50%) scale(1);
}}
#rankBadge.hide{{
    opacity:0;
    transform:translate(-50%,-50%) scale(0.7);
}}
.badge-rank{{
    font-family:'Montserrat',sans-serif;
    font-weight:700; font-size:4.5rem;
    color:#FFD700;
    text-shadow:0 0 40px rgba(255,215,0,0.9), 0 0 80px rgba(255,215,0,0.4);
    letter-spacing:0.1em; line-height:1;
}}
.badge-label{{
    font-size:1rem; color:rgba(212,175,55,0.6);
    letter-spacing:0.4em; text-transform:uppercase;
    margin-top:6px; font-family:'Montserrat',sans-serif;
}}
.badge-name{{
    font-size:2.2rem; font-weight:700;
    color:#FFFFFF;
    text-shadow:0 0 20px rgba(255,255,255,0.6);
    margin-top:14px;
    font-family:'Noto Sans KR',sans-serif;
}}
.badge-tier{{
    font-size:1.3rem; color:rgba(212,175,55,0.8);
    margin-top:6px; letter-spacing:0.05em;
}}

/* TOP7 행 하이라이트 */
.top-row.highlight{{
    background:rgba(212,175,55,0.15);
    border-radius:6px;
    box-shadow:0 0 12px rgba(212,175,55,0.3);
    transition:all 0.4s ease;
}}
</style>
</head>
<body>

<!-- 최상단 타이틀 -->
<div class="header">
  <div class="main-title">✦ &nbsp; WEALTH FA &nbsp; 2026년 2월 &nbsp; ✦</div>
  <div class="update-time">📊 최종 데이터: {metrics['excel_time']}</div>
</div>

<!-- 본문 3열 -->
<div class="body-wrap">

  <!-- ── 좌측 패널 (4카드) -->
  <div class="side-panel">
    <div class="s-card">
      <div class="card-title">ACTIVE FC</div>
      <div class="card-val">{metrics['active_fc']}명</div>
      <div class="card-sub">2월 가동 FC</div>
    </div>
    <div class="s-card">
      <div class="card-title">생명 환산</div>
      <div class="card-val">{fmt_man(metrics['life_hwan'])}</div>
      <div class="card-sub">생명보험 환산보험료</div>
    </div>
    <div class="s-card">
      <div class="card-title">생명 보험료</div>
      <div class="card-val">{fmt_man(metrics['life_prem'])}</div>
      <div class="card-sub">생명보험 보험료 합계</div>
    </div>
    <div class="s-card">
      <div class="card-title">손해 보험료</div>
      <div class="card-val">{fmt_man(metrics['nonlife_prem'])}</div>
      <div class="card-sub">손해보험 보험료 합계</div>
    </div>
  </div>

  <!-- ── 중앙 패널 -->
  <div class="center-panel">
    <div class="date-display">
      <div class="date-label">DATE</div>
      <div class="current-date" id="dateDisplay">2 / 1</div>
    </div>
    <div id="chart"></div>
    <div class="controls">
      <button class="btn active" id="playBtn" onclick="togglePlay()">⏸ 정지</button>
      <button class="btn" onclick="resetAnim()">↺ 처음부터</button>
      <div class="progress-wrap">
        <div class="progress-bg" id="progressBg" onclick="seekAnim(event)">
          <div class="progress-fill" id="progressFill"></div>
        </div>
      </div>
      <span class="speed-label">속도</span>
      <select class="speed-sel" id="speedSel" onchange="changeSpeed()">
        <option value="1200">느리게</option>
        <option value="700" selected>보통</option>
        <option value="300">빠르게</option>
        <option value="80">초고속</option>
      </select>
    </div>
  </div>

  <!-- ── 우측 패널 (TOP7 두 개만) -->
  <div class="side-panel right">
    <div class="s-card grow">
      <div class="card-title">TOP 7 · 월P 실적</div>
      <div class="top-rows">{top7_p_rows()}</div>
    </div>
    <div class="s-card grow">
      <div class="card-title">TOP 7 · 계약 건수</div>
      <div class="top-rows">{top7_cnt_rows()}</div>
    </div>
  </div>

</div><!-- body-wrap -->

<!-- 랭크 뱃지 오버레이 -->
<div id="rankBadge">
  <div class="badge-rank" id="badgeRank">🥇 TOP 1</div>
  <div class="badge-label">WEALTH FA · 2026년 2월</div>
  <div class="badge-name" id="badgeName"></div>
  <div class="badge-tier" id="badgeTier"></div>
</div>

<script>
var chart   = echarts.init(document.getElementById('chart'),null,{{renderer:'canvas'}});
var DATES   = {dates_json};
var FRAMES  = {frames_json};
var TOP7_NAMES = {top7_names_json};
var TOP7_INFO  = {top7_info_json};  // [{{name, tier}}, ...]
var curIdx  = 0, playing = true, timer = null, speed = 1200;
var finaleRunning = false;
window.ANIM_DONE = false;  // 녹화 스크립트가 감지하는 완료 신호

chart.setOption({init_json});
window.addEventListener('resize', function(){{ chart.resize(); }});
setTimeout(startPlay, 2000);

function applyFrame(idx){{
  var f=FRAMES[idx];
  chart.setOption({{animationDurationUpdate:Math.min(speed-50,550),
                    animationEasingUpdate:'cubicOut',series:[{{data:f.nodes,links:f.links}}]}});
  document.getElementById('dateDisplay').innerText=DATES[idx].replace('/',' / ');
  document.getElementById('progressFill').style.width=((idx+1)/DATES.length*100).toFixed(1)+'%';
}}

function startPlay(){{
  if(timer) clearInterval(timer);
  timer=setInterval(function(){{
    if(!playing||finaleRunning) return;
    applyFrame(curIdx); curIdx++;
    if(curIdx>=DATES.length){{
      // 마지막 프레임 완료 → 피날레 시작!
      clearInterval(timer);
      playing=false;
      setTimeout(startFinale, 800);
    }}
  }},speed);
}}

// ══ 피날레: TOP1~7 순서로 별 맥박 애니메이션
function startFinale(){{
  finaleRunning=true;
  var idx=0;
  function next(){{
    if(idx>=TOP7_NAMES.length){{
      // 피날레 완료 → 3초 후 처음부터 재시작
      finaleRunning=false;
      hideBadge();
      window.ANIM_DONE = true;  // 시퀀스 완료 신호!
      setTimeout(function(){{
        curIdx=0; playing=true;
        startPlay();
        var b=document.getElementById('playBtn');
        b.innerText='⏸ 정지'; b.className='btn active';
        window.ANIM_DONE = false;  // 다음 루프 대비 리셋
      }},3000);
      return;
    }}
    var fcName = TOP7_NAMES[idx];
    var rank   = idx+1;
    var info   = TOP7_INFO[idx];

    // 1. 해당 별 크게 펄스
    pulseNode(fcName, rank);

    // 2. 랭크 뱃지 표시
    showBadge(rank, info.name, info.tier);

    // 3. 우측 패널 행 하이라이트
    highlightRow(rank);

    idx++;
    setTimeout(next, 2200);  // 2.2초 간격
  }}
  next();
}}

function pulseNode(fcName, rank){{
  // 마지막 프레임의 노드 복사 후 해당 FC 크기 3배로
  var lastNodes = JSON.parse(JSON.stringify(FRAMES[FRAMES.length-1].nodes));
  for(var i=0;i<lastNodes.length;i++){{
    if(lastNodes[i].name===fcName){{
      var origSize = lastNodes[i].symbolSize;
      lastNodes[i].symbolSize = origSize*3.2;
      lastNodes[i].itemStyle.shadowBlur = 120;
      lastNodes[i].itemStyle.shadowColor='rgba(255,215,0,0.99)';
      lastNodes[i].itemStyle.opacity=1;
      lastNodes[i].itemStyle.borderWidth=3;
      lastNodes[i].itemStyle.borderColor='#FFD700';
      lastNodes[i].label.fontSize=Math.max(12,lastNodes[i].label.fontSize*1.8);
      lastNodes[i].label.color='#FFD700';
      lastNodes[i].label.textShadowBlur=20;
      lastNodes[i].label.textShadowColor='rgba(255,215,0,0.9)';
      break;
    }}
  }}
  chart.setOption({{animationDurationUpdate:500,animationEasingUpdate:'elasticOut',
                    series:[{{data:lastNodes}}]}});
  // 1.5초 후 원상복귀
  setTimeout(function(){{
    chart.setOption({{animationDurationUpdate:400,animationEasingUpdate:'cubicOut',
                      series:[{{data:FRAMES[FRAMES.length-1].nodes}}]}});
  }},1500);
}}

var badgeTimer=null;
function showBadge(rank,name,tier){{
  if(badgeTimer) clearTimeout(badgeTimer);
  var medals=['🥇','🥈','🥉','④','⑤','⑥','⑦'];
  var el=document.getElementById('rankBadge');
  document.getElementById('badgeRank').innerText=medals[rank-1]+' TOP '+rank;
  document.getElementById('badgeName').innerText=name;
  document.getElementById('badgeTier').innerText=tier;
  el.className='show';
  badgeTimer=setTimeout(function(){{el.className='hide';}},1800);
}}
function hideBadge(){{
  document.getElementById('rankBadge').className='hide';
}}
function highlightRow(rank){{
  // 모든 top-row에서 하이라이트 제거 후 해당 rank 행만 강조
  var rows=document.querySelectorAll('.top-row');
  rows.forEach(function(r){{r.classList.remove('highlight');}});
  // rank번째 행 선택 (월P TOP7 기준 - 첫 7개)
  var target=document.querySelectorAll('.s-card.grow:first-of-type .top-row')[rank-1];
  if(target) target.classList.add('highlight');
  setTimeout(function(){{
    if(target) target.classList.remove('highlight');
  }},1800);
}}

function togglePlay(){{
  if(finaleRunning) return;
  playing=!playing;
  var b=document.getElementById('playBtn');
  b.innerText=playing?'⏸ 정지':'▶ 재생'; b.className=playing?'btn active':'btn';
  if(playing) startPlay();
}}
function resetAnim(){{
  finaleRunning=false; hideBadge();
  curIdx=0;playing=true;
  document.getElementById('playBtn').innerText='⏸ 정지';
  document.getElementById('playBtn').className='btn active';
  applyFrame(0); startPlay();
}}
function changeSpeed(){{ speed=parseInt(document.getElementById('speedSel').value); if(playing) startPlay(); }}
function seekAnim(e){{
  if(finaleRunning) return;
  var r=document.getElementById('progressBg').getBoundingClientRect();
  curIdx=Math.max(0,Math.min(Math.floor((e.clientX-r.left)/r.width*DATES.length),DATES.length-1));
  applyFrame(curIdx);
}}
</script>
</body>
</html>"""

def main():
    print("데이터 로드 중...")
    all_fcs, all_dates, cumul, global_max, metrics = load()
    print(f"  FC: {len(all_fcs)}명 / {len(all_dates)}일 / Excel: {metrics['excel_time']}")
    html = build_html(all_fcs, all_dates, cumul, global_max, metrics)
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"SUCCESS: {OUT_HTML}")

if __name__ == "__main__":
    main()
