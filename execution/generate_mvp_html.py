"""
월별 MVP Eclipse Reveal HTML 자동 생성기 + 동영상 변환
1단계: 엑셀 데이터 → MVP 추출
2단계: HTML 생성
3단계: Playwright로 22초 녹화 (WebM)
4단계: moviepy로 MP4 변환
실행: python execution/generate_mvp_html.py
"""
import pandas as pd
import os, sys, time, glob, shutil, subprocess, datetime

sys.stdout.reconfigure(encoding='utf-8')

# ══════════════════════════════════════════════════
# ★ 설정값 (필요시 여기만 수정)
# ══════════════════════════════════════════════════
BASE     = os.path.dirname(os.path.abspath(__file__))
EXCEL    = os.path.join(BASE, "..", "매일업데이트", "26년종합.xlsx")
OUT_DIR  = os.path.join(BASE, "..", "매일업데이트")
EXCLUDE_FC = ['임정일']   # TOP 집계 제외 FC

# 대상 연/월 (None이면 오늘 기준 자동)
TARGET_YEAR  = None   # None = 자동(전월 기준)
TARGET_MONTH = None   # None = 자동(전월 기준)

# ══════════════════════════════════════════════════
# 1. 데이터 로드 & MVP 계산
# ══════════════════════════════════════════════════
def get_mvp(year=None, month=None):
    now = datetime.datetime.now()
    # None이면 자동으로 전월을 기준으로 사용 (매월 월쉤 MVP 실행 시)
    if year is None or month is None:
        prev = (now.replace(day=1) - datetime.timedelta(days=1))  # 전월 마지막 날
        year  = prev.year
        month = prev.month

    raw = pd.read_excel(EXCEL, sheet_name="RAWDATA")
    raw['FC명']     = raw.iloc[:, 2]
    raw['계약일자'] = pd.to_datetime(raw.iloc[:, 11], errors='coerce')
    p1 = pd.to_numeric(raw.iloc[:, 15].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    p2 = pd.to_numeric(raw.iloc[:, 16].astype(str).str.replace(',',''), errors='coerce').fillna(0)
    raw['월P'] = p1 + p2

    df = raw[
        (raw['계약일자'].dt.year  == year) &
        (raw['계약일자'].dt.month == month) &
        (~raw['FC명'].isin(EXCLUDE_FC))
    ]

    # 월P MVP
    top_p   = df.groupby('FC명')['월P'].sum().sort_values(ascending=False)
    mvp_p   = top_p.index[0] if len(top_p) > 0 else "해당 없음"

    # 활동(건수) MVP
    top_cnt = df.groupby('FC명').size().sort_values(ascending=False)
    mvp_cnt_name = top_cnt.index[0]  if len(top_cnt) > 0 else "해당 없음"
    mvp_cnt_val  = int(top_cnt.iloc[0]) if len(top_cnt) > 0 else 0

    # 한글 월 레이블
    month_label = f"{str(year)[-2:]}년 {month}월"

    print(f"[{month_label}] 월P MVP: {mvp_p}  /  활동 MVP: {mvp_cnt_name} ({mvp_cnt_val}건)")
    return year, month, month_label, mvp_p, mvp_cnt_name, mvp_cnt_val

# ══════════════════════════════════════════════════
# 2. HTML 생성
# ══════════════════════════════════════════════════
def build_html(month_label, mvp_p_name, mvp_cnt_name, mvp_cnt_val):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{month_label} 웰스 MVP · Eclipse Reveal</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;700;900&family=Montserrat:wght@100;300;700;900&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{
  width:100%; height:100%;
  background:#000;
  color:#fff;
  font-family:'Noto Sans KR','Montserrat',sans-serif;
  overflow:hidden;
  cursor:none;
}}

/* 배경 별 */
.star {{
  position:fixed; border-radius:50%;
  background:rgba(212,175,55,0.55);
  animation:twinkle var(--d,3s) ease-in-out infinite alternate;
}}
@keyframes twinkle {{
  from {{ opacity:0.08; transform:scale(0.8); }}
  to   {{ opacity:0.65; transform:scale(1.2); }}
}}

/* PHASE 1 */
#phase1 {{
  position:fixed; inset:0;
  display:flex; align-items:center; justify-content:center;
  opacity:0; z-index:10;
}}

/* 트로피 래퍼 */
.eclipse-moon {{
  position:relative;
  display:flex; align-items:center; justify-content:center;
  z-index:2;
  filter:drop-shadow(0 0 0px rgba(212,175,55,0));
}}
.trophy-svg {{
  width:clamp(330px,42vw,540px); height:auto; display:block;
}}

/* 코로나 맥동 */
@keyframes glow-pulse {{
  0%,100% {{ filter:
    drop-shadow(0 0 18px rgba(212,175,55,0.70))
    drop-shadow(0 0 50px rgba(212,175,55,0.40))
    drop-shadow(0 0 100px rgba(255,200,50,0.18)); }}
  50% {{ filter:
    drop-shadow(0 0 38px rgba(255,220,60,1))
    drop-shadow(0 0 90px rgba(212,175,55,0.70))
    drop-shadow(0 0 180px rgba(255,200,50,0.35)); }}
}}
/* 코로나 최대 폭발 */
@keyframes glow-explode {{
  0%   {{ filter:
    drop-shadow(0 0 50px rgba(255,230,80,1))
    drop-shadow(0 0 120px rgba(212,175,55,0.85))
    drop-shadow(0 0 240px rgba(255,180,30,0.45)); }}
  100% {{ filter:
    drop-shadow(0 0 80px rgba(255,240,100,1))
    drop-shadow(0 0 180px rgba(212,175,55,1))
    drop-shadow(0 0 360px rgba(255,180,30,0.60)); }}
}}

/* 텍스트 */
.eclipse-text {{
  position:absolute;
  top:28%; left:50%;
  transform:translateX(-50%);
  text-align:center; white-space:nowrap;
  opacity:0; z-index:3;
  background:linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #D4AF37 60%, #B8860B 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  filter:none;
}}
.eclipse-text .main-line {{
  display:block;
  font-family:'Noto Sans KR',sans-serif;
  font-weight:900;
  font-size:clamp(4.5rem,10.125vw,8.1rem);
  letter-spacing:0.22em;
  line-height:1.25;
}}
.eclipse-text .sub-line {{
  display:block;
  font-family:'Montserrat',sans-serif;
  font-weight:300;
  font-size:clamp(1.575rem,2.7vw,2.25rem);
  letter-spacing:0.55em;
  margin-top:14px;
  background:linear-gradient(90deg, rgba(212,175,55,0.5), rgba(255,215,0,0.9), rgba(212,175,55,0.5));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  filter:none;
}}

/* 화면 플래시 */
#flash {{
  position:fixed; inset:0;
  background:radial-gradient(ellipse 70% 70% at 50% 50%, rgba(255,220,80,0) 0%, rgba(255,220,80,0) 100%);
  pointer-events:none; z-index:6;
  transition:background 1.5s ease;
}}

/* PHASE 2 */
#phase2 {{
  position:fixed; inset:0;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  opacity:0; z-index:10;
}}

/* Phase2 상단 타이틀 */
.p2-header {{
  flex-shrink:0;
  text-align:center; white-space:nowrap;
  margin-top:6vh;
  padding-bottom:28px;
  opacity:0;
  background:linear-gradient(180deg, #FFF8DC 0%, #FFD700 30%, #D4AF37 60%, #B8860B 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  filter:drop-shadow(0 0 22px rgba(255,215,0,0.85)) drop-shadow(0 0 55px rgba(212,175,55,0.55));
}}
.p2-header .p2-main {{
  display:block;
  font-family:'Noto Sans KR',sans-serif;
  font-weight:900;
  font-size:clamp(2.4rem,4.5vw,4.2rem);
  letter-spacing:0.22em;
  line-height:1.2;
}}
.p2-header .p2-sub {{
  display:block;
  font-family:'Montserrat',sans-serif;
  font-weight:300;
  font-size:clamp(0.9rem,1.5vw,1.275rem);
  letter-spacing:0.55em;
  margin-top:8px;
  background:linear-gradient(90deg, rgba(212,175,55,0.4), rgba(255,215,0,0.8), rgba(212,175,55,0.4));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  filter:none;
}}

/* 패널 행 래퍼 */
.p2-body {{
  display:flex; align-items:center; justify-content:center;
  width:100%; flex:1;
}}
.mvp-panel {{
  flex:1; height:100%;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:40px 40px; opacity:0;
}}
.divider {{
  width:1px; height:60vh;
  background:linear-gradient(to bottom, transparent, rgba(212,175,55,0.3) 30%, rgba(212,175,55,0.3) 70%, transparent);
  align-self:center; flex-shrink:0; opacity:0;
}}
.panel-badge {{
  font-family:'Montserrat',sans-serif; font-weight:900;
  font-size:clamp(1.125rem,1.8vw,1.5rem);
  letter-spacing:0.5em; text-transform:uppercase;
  margin-bottom:18px; opacity:0.85;
}}
.panel-badge.gold {{ color:#D4AF37; }}
.panel-badge.blue {{ color:#6ECFFF; }}
.panel-label {{
  font-family:'Noto Sans KR',sans-serif; font-weight:900;
  font-size:clamp(1.275rem,2.1vw,1.65rem);
  letter-spacing:0.25em; margin-bottom:28px;
  color:rgba(255,255,255,0.75);
}}
.mvp-crown {{ font-size:clamp(4.2rem,6vw,5.7rem); margin-bottom:14px; }}
.mvp-name {{
  font-family:'Noto Sans KR',sans-serif; font-weight:900;
  font-size:clamp(4.5rem,9.75vw,8.7rem);
  line-height:1; letter-spacing:0.06em; margin-bottom:26px;
}}
.mvp-name.gold {{
  color:#FFD700;
  text-shadow:0 0 16px rgba(255,215,0,0.9), 0 0 40px rgba(212,175,55,0.7),
              0 0 90px rgba(212,175,55,0.3), 0 0 160px rgba(212,175,55,0.1);
}}
.mvp-name.blue {{
  color:#A8EEFF;
  text-shadow:0 0 16px rgba(110,207,255,0.95), 0 0 40px rgba(110,207,255,0.65),
              0 0 90px rgba(110,207,255,0.3), 0 0 160px rgba(110,207,255,0.1);
}}
.mvp-value {{
  font-family:'Montserrat',sans-serif; font-weight:700;
  font-size:clamp(1.95rem,3.75vw,3rem); letter-spacing:0.08em;
  color:rgba(255,255,255,0.55);
}}
.mvp-value .num {{ color:#FFD700; font-size:1.3em; }}
.mvp-value .unit {{ color:rgba(212,175,55,0.6); font-size:0.8em; }}

/* PHASE 3: 브리딩 */
@keyframes breathe-gold {{
  0%,100% {{ text-shadow:0 0 16px rgba(255,215,0,0.9), 0 0 40px rgba(212,175,55,0.7), 0 0 90px rgba(212,175,55,0.3); }}
  50%     {{ text-shadow:0 0 30px rgba(255,215,0,1), 0 0 70px rgba(212,175,55,1), 0 0 140px rgba(212,175,55,0.6), 0 0 220px rgba(212,175,55,0.2); }}
}}
@keyframes breathe-blue {{
  0%,100% {{ text-shadow:0 0 16px rgba(110,207,255,0.95), 0 0 40px rgba(110,207,255,0.65), 0 0 90px rgba(110,207,255,0.3); }}
  50%     {{ text-shadow:0 0 30px rgba(110,207,255,1), 0 0 70px rgba(110,207,255,0.9), 0 0 140px rgba(110,207,255,0.5), 0 0 220px rgba(110,207,255,0.2); }}
}}
.breathing-gold {{ animation:breathe-gold 2.8s ease-in-out infinite; }}
.breathing-blue {{ animation:breathe-blue 2.8s ease-in-out infinite 0.5s; }}

/* 오버레이 */
#overlay {{
  position:fixed; inset:0;
  background:#000; z-index:100; opacity:1; pointer-events:none;
}}
#watermark {{
  position:fixed; bottom:22px; right:34px;
  font-family:'Montserrat',sans-serif; font-weight:100;
  font-size:1.05rem; color:rgba(212,175,55,0.15);
  letter-spacing:0.3em; z-index:20;
}}
</style>
</head>
<body>

<div id="flash"></div>
<div id="overlay"></div>

<!-- PHASE 1 -->
<div id="phase1">
  <div class="eclipse-moon" id="moon">
    <svg class="trophy-svg" viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
      <path d="M52 18 H148 V98 C148 138 106 158 100 158 C94 158 52 138 52 98 Z"
            fill="#080808" stroke="rgba(212,175,55,0.15)" stroke-width="1.5"/>
      <path d="M52 36 C22 36 16 70 30 86 C38 95 52 90 52 90"
            fill="none" stroke="rgba(212,175,55,0.15)" stroke-width="3" stroke-linecap="round"/>
      <path d="M148 36 C178 36 184 70 170 86 C162 95 148 90 148 90"
            fill="none" stroke="rgba(212,175,55,0.15)" stroke-width="3" stroke-linecap="round"/>
      <rect x="87" y="158" width="26" height="40" fill="#080808" stroke="rgba(212,175,55,0.10)" stroke-width="1"/>
      <rect x="52" y="198" width="96" height="16" rx="4" fill="#080808" stroke="rgba(212,175,55,0.15)" stroke-width="1.2"/>
      <rect x="38" y="214" width="124" height="14" rx="5" fill="#080808" stroke="rgba(212,175,55,0.15)" stroke-width="1.2"/>
      <path d="M52 98 Q100 115 148 98" fill="none" stroke="rgba(212,175,55,0.10)" stroke-width="1"/>
    </svg>
    <div class="eclipse-text" id="eclipse-text">
      <span class="main-line">{month_label}<br>웰스 MVP</span>
      <span class="sub-line">WEALTH FA · MONTHLY MVP</span>
    </div>
  </div>
</div>

<!-- PHASE 2 -->
<div id="phase2">
  <!-- 상단 타이틀 (Phase1 텍스트와 동일 스타일) -->
  <div class="p2-header" id="p2-header">
    <span class="p2-main">{month_label} 웰스 MVP</span>
    <span class="p2-sub">WEALTH FA · MONTHLY MVP</span>
  </div>
  <!-- 좌우 MVP 패널 -->
  <div class="p2-body">
    <div class="mvp-panel" id="panel-p">
      <div class="panel-badge gold">Monthly P</div>
      <div class="panel-label">월 실적 MVP</div>
      <div class="mvp-crown">🏆</div>
      <div class="mvp-name gold" id="name-p">{mvp_p_name}</div>
    </div>
    <div class="divider" id="divider"></div>
    <div class="mvp-panel" id="panel-c">
      <div class="panel-badge blue">Activity</div>
      <div class="panel-label">활동 MVP</div>
      <div class="mvp-crown">⚡</div>
      <div class="mvp-name blue" id="name-c">{mvp_cnt_name}</div>
      <div class="mvp-value">
        <span class="num">{mvp_cnt_val}</span><span class="unit"> 건</span>
      </div>
    </div>
  </div>
</div>

<div id="watermark">WEALTH FA · {month_label}</div>

<script>
(function(){{
  for(var i=0;i<65;i++){{
    var s=document.createElement('div'); s.className='star';
    var sz=Math.random()*2+0.8;
    s.style.cssText='width:'+sz+'px;height:'+sz+'px;top:'+(Math.random()*100)+'%;left:'+(Math.random()*100)+'%;--d:'+(Math.random()*4+2).toFixed(1)+'s;animation-delay:'+(Math.random()*6).toFixed(1)+'s;';
    document.body.appendChild(s);
  }}
}})();

var overlay=document.getElementById('overlay');
var phase1=document.getElementById('phase1');
var phase2=document.getElementById('phase2');
var moon=document.getElementById('moon');
var eclText=document.getElementById('eclipse-text');
var flash=document.getElementById('flash');
var p2Header=document.getElementById('p2-header');
var panelP=document.getElementById('panel-p');
var panelC=document.getElementById('panel-c');
var divider=document.getElementById('divider');
var nameP=document.getElementById('name-p');
var nameC=document.getElementById('name-c');

function runTimeline(){{
  overlay.style.transition='none'; overlay.style.opacity='1';
  phase1.style.transition='none'; phase1.style.opacity='0';
  phase2.style.transition='none'; phase2.style.opacity='0';
  p2Header.style.transition='none'; p2Header.style.opacity='0';
  panelP.style.transition='none'; panelP.style.opacity='0';
  panelC.style.transition='none'; panelC.style.opacity='0';
  divider.style.transition='none'; divider.style.opacity='0';
  moon.style.animation='none'; moon.style.filter='none';
  eclText.style.animation='none'; eclText.style.opacity='0'; eclText.style.filter='none';
  flash.style.transition='none';
  flash.style.background='radial-gradient(ellipse 70% 70% at 50% 50%,rgba(255,220,80,0)0%,rgba(255,220,80,0)100%)';
  nameP.classList.remove('breathing-gold');
  nameC.classList.remove('breathing-blue');

  // 0.3s: 오버레이 아웃
  setTimeout(function(){{
    overlay.style.transition='opacity 0.7s ease';
    overlay.style.opacity='0';
  }},300);

  // 0.8s: Phase1 트로피 등장
  setTimeout(function(){{
    phase1.style.transition='opacity 0.5s ease';
    phase1.style.opacity='1';
    moon.style.filter='none';
  }},800);

  // 1.0s: 코로나 발화
  setTimeout(function(){{
    moon.style.transition='filter 1.2s ease';
    moon.style.filter='drop-shadow(0 0 20px rgba(212,175,55,0.65)) drop-shadow(0 0 55px rgba(212,175,55,0.35)) drop-shadow(0 0 120px rgba(255,200,50,0.16))';
    setTimeout(function(){{ moon.style.animation='glow-pulse 1.6s ease-in-out infinite'; }},1200);
  }},1000);

  // 3.0s: 텍스트 즉시 등장
  setTimeout(function(){{
    eclText.style.transition='none';
    eclText.style.opacity='1';
    eclText.style.filter='drop-shadow(0 0 28px rgba(255,215,0,0.95)) drop-shadow(0 0 65px rgba(212,175,55,0.65))';
  }},3000);

  // 5.0s: 절정 발광
  setTimeout(function(){{
    moon.style.animation='glow-explode 1.5s ease-in-out infinite alternate';
    flash.style.transition='background 1s ease';
    flash.style.background='radial-gradient(ellipse 65% 65% at 50% 50%,rgba(255,210,60,0.08)0%,transparent 70%)';
    eclText.style.filter='drop-shadow(0 0 40px rgba(255,230,80,1)) drop-shadow(0 0 100px rgba(212,175,55,0.9))';
  }},5000);

  // 6.5s: 크로스페이드 → Phase2 (헤더 포함)
  setTimeout(function(){{
    phase2.style.transition='opacity 0.1s'; phase2.style.opacity='1';
    phase1.style.transition='opacity 1.4s ease'; phase1.style.opacity='0';
    flash.style.transition='background 1.2s ease';
    flash.style.background='radial-gradient(ellipse 70% 70% at 50% 50%,rgba(255,220,80,0.03)0%,transparent 70%)';
    // 상단 타이틀 헤더 등장 (phase2와 동시)
    p2Header.style.transition='opacity 1.0s ease';
    p2Header.style.opacity='1';
  }},6500);

  // 7.0s: 좌 패널
  setTimeout(function(){{ panelP.style.transition='opacity 1.3s ease'; panelP.style.opacity='1'; }},7000);
  // 7.8s: 분리선
  setTimeout(function(){{ divider.style.transition='opacity 0.9s ease'; divider.style.opacity='1'; }},7800);
  // 8.4s: 우 패널
  setTimeout(function(){{ panelC.style.transition='opacity 1.3s ease'; panelC.style.opacity='1'; }},8400);

  // 12.0s: Phase 3 — 브리딩 글로우 (이후 루프/블랙아웃 없이 영상 종료)
  setTimeout(function(){{
    nameP.classList.add('breathing-gold');
    nameC.classList.add('breathing-blue');
    flash.style.transition='background 2s ease';
    flash.style.background='radial-gradient(ellipse 90% 90% at 50% 50%,rgba(212,175,55,0.04)0%,transparent 70%)';
  }},12000);

  // ★ 블랙아웃 없음 — Phase3 브리딩 글로우 상태로 영상 종료
}}

runTimeline();

// 더블클릭 → 전체화면
document.addEventListener('dblclick',function(){{
  if(!document.fullscreenElement) document.documentElement.requestFullscreen();
  else document.exitFullscreen();
}});
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════
# 3. Playwright 22초 녹화 → WebM 저장
# ══════════════════════════════════════════════════
RECORD_SEC = 20   # 12s(Phase3 시작) + 8초 브리딩 글로우 후 종료

def record_video(html_path, out_dir, now_str):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ playwright 없음. 설치: pip install playwright && playwright install chromium")
        return None

    webm_dir = os.path.join(out_dir, "_mvp_video_tmp")
    os.makedirs(webm_dir, exist_ok=True)

    print(f"\n🎬 브라우저 열고 {RECORD_SEC}초 녹화 시작...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized","--disable-infobars"])
        context = browser.new_context(
            viewport={"width":1920,"height":1080},
            record_video_dir=webm_dir,
            record_video_size={"width":1920,"height":1080},
        )
        page = context.new_page()
        url = "file:///" + html_path.replace("\\", "/")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)

        print(f"⏱️  {RECORD_SEC}초 녹화 중...")
        bar_len = 40
        for i in range(RECORD_SEC):
            time.sleep(1)
            filled = int(bar_len * (i+1) / RECORD_SEC)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r  [{bar}] {i+1:2d}/{RECORD_SEC}초", end="", flush=True)

        print("\n✅ 녹화 완료! 저장 중...")
        context.close()
        browser.close()

    webm_files = sorted(glob.glob(os.path.join(webm_dir, "*.webm")), key=os.path.getmtime, reverse=True)
    if not webm_files:
        print("❌ 녹화 파일을 찾을 수 없습니다.")
        return None

    dest_webm = os.path.join(out_dir, f"MVP_Eclipse_{now_str}.webm")
    shutil.move(webm_files[0], dest_webm)
    try: shutil.rmtree(webm_dir)
    except: pass
    return dest_webm

# ══════════════════════════════════════════════════
# 4. WebM → MP4 변환
# ══════════════════════════════════════════════════
def convert_mp4(webm_path):
    mp4_path = webm_path.replace(".webm", ".mp4")
    print("\n🔄 MP4 변환 중...")
    try:
        from moviepy import VideoFileClip
        clip = VideoFileClip(webm_path)
        clip.write_videofile(mp4_path, codec="libx264", fps=24, preset="fast", audio=False, logger="bar")
        clip.close()
        if os.path.exists(mp4_path):
            size_mb = os.path.getsize(mp4_path) / (1024*1024)
            print(f"✅ MP4 저장 완료! ({size_mb:.1f} MB)")
            os.remove(webm_path)
            return mp4_path
    except Exception as e:
        print(f"⚠️  변환 실패: {e} → WebM 유지")
    return webm_path

# ══════════════════════════════════════════════════
# 5. 통합 실행
# ══════════════════════════════════════════════════
def main():
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 55)
    print("  MVP Eclipse Reveal · HTML + 동영상 자동 생성")
    print("=" * 55)

    # 1단계: MVP 데이터 추출
    print("\n[1/4] 📊 Maven 데이터 추출 중...")
    year, month, month_label, mvp_p, mvp_cnt_name, mvp_cnt_val = get_mvp(TARGET_YEAR, TARGET_MONTH)

    # 2단계: HTML 생성
    print("\n[2/4] 📄 HTML 생성 중...")
    html = build_html(month_label, mvp_p, mvp_cnt_name, mvp_cnt_val)
    fname_html = f"MVP_Eclipse_{year}{month:02d}.html"
    out_path = os.path.abspath(os.path.join(OUT_DIR, fname_html))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"   ✅ HTML: {out_path}")

    # 3단계: 녹화
    print("\n[3/4] 🎬 동영상 녹화...")
    webm_path = record_video(out_path, os.path.abspath(OUT_DIR), now_str)
    if not webm_path:
        sys.exit(1)

    # 4단계: MP4 변환
    print("\n[4/4] 🎞️  MP4 변환...")
    final_path = convert_mp4(webm_path)

    print()
    print("=" * 55)
    print("  🎉 전체 완료!")
    print(f"  📄 HTML : {fname_html}")
    print(f"  🎬 동영상: {os.path.basename(final_path)}")
    print(f"  📁 폴더  : {os.path.dirname(final_path)}")
    print("=" * 55)

    # 탐색기에서 파일 선택
    subprocess.Popen(f'explorer /select,"{final_path}"')

if __name__ == "__main__":
    main()

