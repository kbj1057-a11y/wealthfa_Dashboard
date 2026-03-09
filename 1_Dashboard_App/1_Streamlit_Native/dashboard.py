
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="웰스FA 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="auto"
)

# ─────────────────────────────────────────────
# 글로벌 CSS — VVIP Dark Gold Glass Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:wght@700;900&display=swap');

/* ══ 전역 리셋 & 기반 ══════════════════════════════ */
*, *::before, *::after {
    font-family: 'Noto Sans KR', sans-serif !important;
    box-sizing: border-box;
    margin: 0; padding: 0;
}

/* ══ 모바일용 카드 스타일 ═══════════════════════════ */
.mobile-card {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    margin-bottom: 10px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
}
.m-label { color: #A0A0A0; font-size: 0.82rem; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.m-value { color: #f5d061; font-size: 1.5rem; font-weight: 900; line-height: 1.2; }
.m-sub { color: #667788; font-size: 0.78rem; margin-top: 4px; }

/* ══ 앱 배경 — 딥 차콜 그라데이션 ════════════════ */
.stApp {
    background: linear-gradient(160deg, #1a1610 0%, #121212 45%, #0f0f0f 100%) !important;
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(212,175,55,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(212,175,55,0.04) 0%, transparent 50%);
    pointer-events: none; z-index: 0;
}

/* ══ Streamlit 기본 UI 오염 제거 ════════════════ */
.block-container {
    padding: 1rem 2rem 4rem 2rem !important;
    max-width: 1600px !important;
    position: relative; z-index: 1;
}
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] {
    background: rgba(15,15,15,0.95) !important;
}

/* ══ 사이드바 화살표 텍스트Artifact 제거 ══════════ */
[data-testid="stSidebarCollapseButton"] div,
[data-testid="stSidebarCollapseButton"] span {
    font-size: 0 !important;
    line-height: 0 !important;
    color: transparent !important;
}
[data-testid="stSidebarCollapseButton"] svg {
    width: 1.2rem !important;
    height: 1.2rem !important;
    fill: #D4AF37 !important;
}

/* ══ 버튼 스타일 (VVIP GOLD - 초강력 고정) ══════════════════════════════════ */
/* 모든 종류의 Streamlit 버튼을 다크 골드로 강제 전환 */
button[data-testid^="baseButton"], 
button[kind="secondary"],
button[kind="primary"],
.stButton button,
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #262118 0%, #1a1610 100%) !important;
    background-color: #1a1610 !important;
    border: 1px solid rgba(212,175,55,0.7) !important;
    color: #f5d061 !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.9) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
    cursor: pointer !important;
}

/* 호버 시 골드 발광 효과 */
button[data-testid^="baseButton"]:hover, 
.stButton button:hover,
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #443c2a 0%, #262118 100%) !important;
    border-color: #F5D061 !important;
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(212,175,55,0.4) !important;
    transform: translateY(-2px) !important;
}

/* 글자색 강제 고정 (Span, P 태그 대응) */
button[data-testid^="baseButton"] span,
button[data-testid^="baseButton"] p,
.stButton button span,
.stButton button p,
div[data-testid="stButton"] button span,
div[data-testid="stButton"] button p {
    color: #f5d061 !important;
    font-weight: 800 !important;
    text-decoration: none !important;
}

button[data-testid^="baseButton"]:hover span,
button[data-testid^="baseButton"]:hover p,
.stButton button:hover span,
.stButton button:hover p {
    color: #ffffff !important;
}

/* ══ 레이아웃 개선 ══════════════════════════════════ */
.hero-banner {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg,
        rgba(212,175,55,0.07) 0%,
        transparent 50%,
        rgba(212,175,55,0.03) 100%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #D4AF37, transparent, #D4AF37);
    border-radius: 3px 0 0 3px;
}
.hero-title {
    font-size: 2.8rem; font-weight: 900; letter-spacing: -1px;
    background: linear-gradient(90deg, #D4AF37 0%, #F9A826 50%, #e8cc6a 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.3rem 0; line-height: 1.1;
}
.hero-meta {
    font-size: 0.78rem; color: #A0A0A0;
    letter-spacing: 4px; text-transform: uppercase; margin-bottom: 0.6rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.3);
    color: #D4AF37; font-size: 0.72rem; font-weight: 700;
    padding: 0.28rem 0.9rem; border-radius: 20px;
    letter-spacing: 0.5px;
}

/* ══ 섹션 타이틀 ════════════════════════════ */
.section-title {
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 1.2rem; color: #D4AF37;
    display: flex; align-items: center; gap: 0.6rem;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(212,175,55,0.3), transparent);
}

/* ══ 글래스 패널 (리더보드 / 차트 공통) ════ */
.glass-panel {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(212,175,55,0.15);
    border-radius: 20px;
    padding: 1.6rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    transition: border-color 0.3s, box-shadow 0.3s;
    height: 100%;
}
.glass-panel:hover {
    border-color: rgba(212,175,55,0.35);
    box-shadow: 0 12px 40px rgba(0,0,0,0.6), 0 0 20px rgba(212,175,55,0.08);
}

/* board 별칭 */
.board-wrap { background: rgba(255,255,255,0.03); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; padding: 1.6rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5); transition: border-color 0.3s, box-shadow 0.3s; }
.board-wrap:hover { border-color: rgba(212,175,55,0.35); box-shadow: 0 12px 40px rgba(0,0,0,0.6), 0 0 20px rgba(212,175,55,0.08); }
.chart-box { background: rgba(255,255,255,0.03); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; padding: 1.6rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5); }

.board-header {
    font-size: 0.9rem; font-weight: 800; margin-bottom: 1.2rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid rgba(212,175,55,0.12);
    letter-spacing: 0.5px;
}

/* ══ 랭크 행 ════════════════════════════════ */
.rank-row {
    display: flex; align-items: center; gap: 1rem;
    padding: 0.7rem 1rem; border-radius: 12px; margin-bottom: 0.5rem;
    transition: transform 0.2s ease, border-color 0.2s ease,
                box-shadow 0.2s ease, background 0.2s ease;
    cursor: default; border: 1px solid transparent;
}
.rank-row:hover {
    transform: translateY(-3px) translateX(4px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
}

/* 1위: 골드 글로우 */
.r1 {
    background: linear-gradient(90deg,rgba(212,175,55,0.18) 0%,rgba(212,175,55,0.04) 100%);
    border-left: 3px solid #D4AF37 !important; border-radius: 0 12px 12px 0;
}
.r1:hover { border-color: rgba(212,175,55,0.6); box-shadow: 0 6px 24px rgba(212,175,55,0.15); }
/* 2위: 실버 */
.r2 {
    background: linear-gradient(90deg,rgba(192,192,192,0.13) 0%,transparent 100%);
    border-left: 3px solid #C0C0C0 !important; border-radius: 0 12px 12px 0;
}
.r2:hover { border-color: rgba(192,192,192,0.5); }
/* 3위: 브론즈 */
.r3 {
    background: linear-gradient(90deg,rgba(205,127,50,0.13) 0%,transparent 100%);
    border-left: 3px solid #CD7F32 !important; border-radius: 0 12px 12px 0;
}
.r3:hover { border-color: rgba(205,127,50,0.5); }
/* 4~7위 */
.rx {
    background: rgba(255,255,255,0.02);
    border-left: 3px solid rgba(255,255,255,0.06) !important; border-radius: 0 12px 12px 0;
}
.rx:hover { border-color: rgba(212,175,55,0.3); background: rgba(212,175,55,0.04); }

/* 순위 숫자 */
.rnum { width: 2.2rem; font-size: 1.25rem; font-weight: 900; text-align: center; flex-shrink: 0; }
.r1 .rnum { color: #D4AF37; text-shadow: 0 0 12px rgba(212,175,55,0.6); }
.r2 .rnum { color: #C0C0C0; }
.r3 .rnum { color: #CD7F32; }
.rx .rnum { color: rgba(255,255,255,0.2); }

.rinfo { flex: 1; min-width: 0; }
.rname {
    font-size: 0.95rem; font-weight: 700; color: #FFFFFF;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    letter-spacing: 0.3px;
}
.rgrade { font-size: 0.7rem; color: #606060; margin-top: 2px; }
.rval { font-weight: 900; text-align: right; white-space: nowrap; flex-shrink: 0; }

/* ══ KPI 카드 ════════════════════════════════ */
.kpi-box {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(212,175,55,0.15);
    border-radius: 18px; padding: 1.4rem 1.6rem; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}
.kpi-box:hover {
    border-color: rgba(212,175,55,0.45);
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 20px rgba(212,175,55,0.1);
}
.kpi-icon { font-size: 1.6rem; margin-bottom: 0.5rem; }
.kpi-label {
    font-size: 0.68rem; color: #A0A0A0;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.5rem;
}
.kpi-val { font-size: 2rem; font-weight: 900; color: #FFFFFF; line-height: 1; }
.kpi-sub { font-size: 0.7rem; margin-top: 0.4rem; }

/* ══ 목표 달성 프로그레스 바 ════════════════ */
@keyframes fillGold {
    0%   { width: 0%; box-shadow: none; }
    60%  { box-shadow: 0 0 8px rgba(212,175,55,0.7); }
    100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); }
}
.prog-bar {
    height: 10px; background: rgba(255,255,255,0.06);
    border-radius: 5px; overflow: visible;
    position: relative;
}
.prog-fill {
    height: 100%; border-radius: 5px;
    background: linear-gradient(90deg, #8B6914 0%, #D4AF37 60%, #F9E080 100%);
    animation: fillGold 1.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    box-shadow: 0 0 10px rgba(212,175,55,0.5);
}
.prog-fill::after {
    content: '';
    position: absolute; right: -2px; top: -3px;
    width: 16px; height: 16px; border-radius: 50%;
    background: #D4AF37;
    box-shadow: 0 0 10px rgba(212,175,55,0.9), 0 0 20px rgba(212,175,55,0.4);
}

/* ══ 구분선 ════════════════════════════════ */
hr.fancy {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
    margin: 2rem 0;
}


</style>
""", unsafe_allow_html=True)

# ── MVP 버튼 스타일 JavaScript 주입
# Streamlit DOM은 렌더링 후 계속 변경되므로 MutationObserver로 실시간 감지
st.markdown("""
<script>
(function() {
    // 순위별 스타일 정의
    const rankStyles = {
        'mvp-rank-1': {
            background: 'linear-gradient(135deg, rgba(212,175,55,0.18) 0%, rgba(30,25,8,0.95) 100%)',
            borderColor: 'rgba(212,175,55,0.55)',
            color: '#FFE566',
            fontSize: '1.1rem',
            fontWeight: '900',
            textShadow: '0 0 18px rgba(212,175,55,0.6)',
            boxShadow: '0 4px 24px rgba(212,175,55,0.2), inset 0 1px 0 rgba(212,175,55,0.3)'
        },
        'mvp-rank-2': {
            background: 'linear-gradient(135deg, rgba(200,200,200,0.12) 0%, rgba(22,22,28,0.95) 100%)',
            borderColor: 'rgba(200,200,200,0.4)',
            color: '#ECECEC',
            fontSize: '1.05rem',
            fontWeight: '800',
            textShadow: 'none',
            boxShadow: '0 4px 18px rgba(0,0,0,0.45)'
        },
        'mvp-rank-3': {
            background: 'linear-gradient(135deg, rgba(205,127,50,0.14) 0%, rgba(25,18,12,0.95) 100%)',
            borderColor: 'rgba(205,127,50,0.42)',
            color: '#E8C070',
            fontSize: '1.0rem',
            fontWeight: '800',
            textShadow: 'none',
            boxShadow: '0 4px 18px rgba(0,0,0,0.45)'
        },
        'mvp-rank-x': {
            background: 'linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(14,14,18,0.95) 100%)',
            borderColor: 'rgba(100,110,140,0.3)',
            color: '#A8B4C8',
            fontSize: '0.95rem',
            fontWeight: '700',
            textShadow: 'none',
            boxShadow: '0 2px 12px rgba(0,0,0,0.4)'
        }
    };

    const BASE_STYLE = {
        borderRadius: '14px',
        padding: '0.7rem 1.2rem',
        width: '100%',
        textAlign: 'left',
        cursor: 'pointer',
        transition: 'all 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
        backdropFilter: 'blur(14px)',
        WebkitBackdropFilter: 'blur(14px)',
        border: '1px solid',
        fontFamily: "'Noto Sans KR', sans-serif",
        letterSpacing: '0.3px',
        lineHeight: '1.4'
    };

    function applyMvpStyles() {
        // .mvp-name-btn 마커를 모두 찾아서 처리
        document.querySelectorAll('.mvp-name-btn').forEach(function(marker) {
            // 마커가 속한 container (stMarkdownContainer 또는 column 등)
            const markerContainer = marker.closest('[data-testid]');
            if (!markerContainer) return;

            // 해당 컨테이너에서 가장 가까운 stButton 형제를 찾음
            let searchEl = markerContainer;
            let btn = null;

            // 먼저 다음 형제들 중에서 stButton 찾기
            let sibling = searchEl.nextElementSibling;
            while (sibling) {
                const found = sibling.querySelector('button') ||
                    (sibling.dataset.testid === 'stButton' ? sibling.querySelector('button') : null);
                if (found) { btn = found; break; }
                // stButton 자체일 경우
                if (sibling.dataset && sibling.dataset.testid === 'stButton') {
                    btn = sibling.querySelector('button');
                    break;
                }
                sibling = sibling.nextElementSibling;
            }

            // 못 찾으면 부모 column 내에서 stButton 탐색
            if (!btn) {
                const col = marker.closest('[data-testid="column"]');
                if (col) { btn = col.querySelector('[data-testid="stButton"] button'); }
            }

            if (!btn || btn.dataset.mvpStyled === '1') return;

            // 어떤 랭크 클래스인지 판별
            let rankKey = 'mvp-rank-x';
            ['mvp-rank-1','mvp-rank-2','mvp-rank-3','mvp-rank-x'].forEach(function(k) {
                if (marker.classList.contains(k)) rankKey = k;
            });

            const rankStyle = rankStyles[rankKey] || rankStyles['mvp-rank-x'];
            Object.assign(btn.style, BASE_STYLE, {
                background:    rankStyle.background,
                borderColor:   rankStyle.borderColor,
                color:         rankStyle.color,
                fontSize:      rankStyle.fontSize,
                fontWeight:    rankStyle.fontWeight,
                textShadow:    rankStyle.textShadow,
                boxShadow:     rankStyle.boxShadow
            });

            // hover 효과
            btn.addEventListener('mouseenter', function() {
                btn.style.transform = 'translateY(-3px)';
                btn.style.borderColor = 'rgba(212,175,55,0.7)';
                btn.style.boxShadow = '0 10px 32px rgba(0,0,0,0.55), 0 0 22px rgba(212,175,55,0.22)';
            });
            btn.addEventListener('mouseleave', function() {
                btn.style.transform = '';
                btn.style.borderColor = rankStyle.borderColor;
                btn.style.boxShadow = rankStyle.boxShadow;
            });

            btn.dataset.mvpStyled = '1';
        });
    }

    // 초기 실행
    setTimeout(applyMvpStyles, 300);
    setTimeout(applyMvpStyles, 800);
    setTimeout(applyMvpStyles, 1500);

    // DOM 변경 감지 (Streamlit 리렌더링 시 재적용)
    const observer = new MutationObserver(function(mutations) {
        let hasNew = false;
        mutations.forEach(function(m) {
            m.addedNodes.forEach(function(n) {
                if (n.nodeType === 1 && (
                    n.classList?.contains('mvp-name-btn') ||
                    n.querySelector?.('.mvp-name-btn')
                )) hasNew = true;
            });
        });
        if (hasNew) setTimeout(applyMvpStyles, 100);
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
# 로컬과 클라우드 모두에서 파일을 찾기 위한 견고한 경로 탐색
def find_data_file():
    # 1순위: 로컬 절대 경로 (사용자 PC 전용)
    local_abs = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년종합.xlsx"
    if os.path.exists(local_abs): return local_abs
    
    # 2순위: 상대 경로 탐색 (클라우드 환경)
    potential_paths = [
        "매일업데이트/26년종합.xlsx",           # 루트 기준
        "../매일업데이트/26년종합.xlsx",        # execution 폴더 기준 상위
        "execution/매일업데이트/26년종합.xlsx", # 잘못된 깊이 대비
        "26년종합.xlsx"                        # 같은 폴더에 있을 경우
    ]
    
    for path in potential_paths:
        if os.path.exists(path):
            return path
    return None

DATA_FILE = find_data_file()
SHEET_NAME = "RAWDATA"

# 목표 (월별 팀 목표치)
MONTHLY_GOAL_P       = 50_000_000
MONTHLY_GOAL_CASES   = 100

# ─────────────────────────────────────────────
# 데이터 로드
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    if DATA_FILE is None or not os.path.exists(DATA_FILE):
        return None
    try:
        raw = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME, engine='openpyxl')
        n   = len(raw.columns)

        # ── 위치 기반으로 핵심 컬럼 직접 추출 (인코딩 무관)
        def gcol(i, default=None):
            return raw.iloc[:, i] if i < n else pd.Series([default]*len(raw))

        df = pd.DataFrame()
        df['FC명']   = gcol(2)
        df['제휴사']  = gcol(3)  # col[3]: 보험사(제휴사) 이름 — 생명/손해 구분 기준
        df['증권번호'] = gcol(4).astype(str).str.strip()
        df['상품구분'] = gcol(6)
        df['상품명']  = gcol(7)
        df['보험료']  = pd.to_numeric(
            gcol(8).astype(str).str.replace(',','').str.strip(), errors='coerce').fillna(0)
        df['환산1차년'] = pd.to_numeric(
            gcol(9).astype(str).str.replace(',','').str.strip(), errors='coerce').fillna(0)
        df['납입기간'] = gcol(13).astype(str).str.strip()
        df['계약일자'] = pd.to_datetime(gcol(11), errors='coerce')
        
        # ── 수수료 섹션
        df['익월P'] = pd.to_numeric(
            gcol(15).astype(str).str.replace(',','').str.strip(), errors='coerce').fillna(0)
        df['익월시책'] = pd.to_numeric(
            gcol(16).astype(str).str.replace(',','').str.strip(), errors='coerce').fillna(0)
            
        # ── 월P = 초회(익월P) + 익월시책
        df['월P'] = df['익월P'] + df['익월시책']

        # ── 날짜 파생 컬럼
        df['월'] = df['계약일자'].dt.month
        df['연'] = df['계약일자'].dt.year
        df['주'] = df['계약일자'].dt.isocalendar().week.astype('Int64')

        # ── 유효 행만 유지
        df = df[df['FC명'].notna() & (df['증권번호'] != 'nan')].reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return None

# ─────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────
MEDAL = {0: "🥇", 1: "🥈", 2: "🥉"}

def medal(i): return MEDAL.get(i, f"{i+1}")
def rcls(i):  return ["r1","r2","r3"][i] if isinstance(i, int) and i < 3 else "rx"

def p_badge(v):
    """100만 단위로 정확히 표시 (예: 1700만, 1500만)"""
    man = int(v / 10000)  # 만원 단위 절사
    hun = (man // 100) * 100  # 100만 단위 절사
    if   v >= 10_000_000: ic, clr = "💎", "#D4AF37"
    elif v >=  5_000_000: ic, clr = "🔥", "#FF6B6B"
    elif v >=  3_000_000: ic, clr = "⚡", "#FFA040"
    elif v >=  1_000_000: ic, clr = "✨", "#88bbff"
    else:                  ic, clr = "🌱", "#66aa66"
    txt = f"{hun}만P↑" if hun > 0 else f"{man}만P"
    return (ic, clr, txt)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(color="#8899aa", family="Noto Sans KR"),
    margin=dict(l=0, r=0, t=30, b=0),
)
GOLD_SCALE = ["#1a2a4a","#1a3a7a","#2255bb","#FFa040","#FFD700"]

# ─────────────────────────────────────────────
# FC 개인 상세 페이지
# ─────────────────────────────────────────────
def show_fc_detail(fc_name: str, df_all, sel_year: int, sel_month: int, data_time: str):
    """선택된 FC의 전체 상세 실적 페이지."""

    # ── 뒤로 가기 버튼
    col_back, col_title = st.columns([1, 9])
    with col_back:
        if st.button("← 뒤로", key="back_btn", use_container_width=True):
            st.session_state.sel_fc = None
            st.rerun()
    with col_title:
        st.markdown(
            f'<div class="section-title" style="color:#D4AF37;margin-bottom:0;">'
            f'👤 {fc_name} 님의 실적 상세</div>',
            unsafe_allow_html=True
        )

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)

    # ── 데이터 분리
    df_fc_all = df_all[df_all['FC명'] == fc_name].copy()          # 연간 전체
    df_fc_cur = df_all[
        (df_all['FC명'] == fc_name) &
        (df_all['연'] == sel_year) &
        (df_all['월'] == sel_month)
    ].copy()  # 당월

    # ── 당월 KPI
    cur_cases   = len(df_fc_cur)
    cur_mp      = df_fc_cur['월P'].sum()      if '월P'      in df_fc_cur.columns else 0
    cur_prem    = df_fc_cur['보험료'].sum()   if '보험료'   in df_fc_cur.columns else 0
    cur_hwan    = df_fc_cur['환산1차년'].sum() if '환산1차년' in df_fc_cur.columns else 0

    st.markdown(
        f'<div class="section-title" style="color:#88ccff;font-size:1rem;">'
        f'📅 {sel_year}년 {sel_month}월 실적 요약</div>',
        unsafe_allow_html=True
    )
    k1, k2, k3, k4 = st.columns(4)
    kpi_items = [
        (k1, "📋", f"{sel_month}월 계약건수", f"{cur_cases}건", ""),
        (k2, "💎", "생명환산 (환산1차년)", f"{int(cur_hwan/10000):,}만" if cur_hwan else "-", "보험사환산_1차년"),
        (k3, "💰", "월P (초회+익월시책)", f"{int(cur_mp/10000):,}만" if cur_mp else "-", "익월수수료 기준"),
        (k4, "🏦", "월납 보험료", f"{int(cur_prem/10000):,}만" if cur_prem else "-", "합계"),
    ]
    for col, ico, lbl, val, sub in kpi_items:
        with col:
            st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-icon">{ico}</div>
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-val">{val}</div>
                <div class="kpi-sub" style="color:#606060;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)

    # ── 연간 월별 실적 차트
    st.markdown(
        '<div class="section-title" style="color:#88ccff;font-size:1rem;">📊 2026년 월별 실적 추이</div>',
        unsafe_allow_html=True
    )
    if '월' in df_fc_all.columns:
        fc_monthly = (
            df_fc_all[df_fc_all['연'] == sel_year]
            .groupby('월')
            .agg(월P=('월P', 'sum'), 환산=('환산1차년', 'sum'), 건수=('증권번호', 'count'))
            .reset_index()
        )
        fig_m = go.Figure()
        fig_m.add_trace(go.Bar(
            x=fc_monthly['월'], y=fc_monthly['환산'],
            name='환산P', marker_color='rgba(212,175,55,0.55)', yaxis='y1',
            text=[f"{int(v/10000):,}만" for v in fc_monthly['환산']],
            textposition='outside', textfont=dict(color='#D4AF37', size=10),
        ))
        fig_m.add_trace(go.Bar(
            x=fc_monthly['월'], y=fc_monthly['월P'],
            name='월P', marker_color='rgba(136,187,255,0.45)', yaxis='y1',
            text=[f"{int(v/10000):,}만" for v in fc_monthly['월P']],
            textposition='outside', textfont=dict(color='#88bbff', size=10),
        ))
        fig_m.add_trace(go.Scatter(
            x=fc_monthly['월'], y=fc_monthly['건수'],
            name='건수', mode='lines+markers',
            line=dict(color='#FF6B6B', width=2.5),
            marker=dict(size=8), yaxis='y2',
        ))
        fig_m.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
            barmode='group',
            legend=dict(orientation='h', y=1.1, font=dict(color='#8899aa')),
            xaxis=dict(showgrid=False, tickvals=list(range(1,13)),
                       ticktext=[f"{m}월" for m in range(1,13)],
                       tickfont=dict(color='#556677')),
            yaxis =dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                        zeroline=False, tickfont=dict(color='#8899aa')),
            yaxis2=dict(overlaying='y', side='right', showgrid=False,
                        zeroline=False, tickfont=dict(color='#FF6B6B')),
        )
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)

    # ── 당월 계약 명세
    st.markdown(
        f'<div class="section-title" style="color:#88ccff;font-size:1rem;">'
        f'📄 {sel_month}월 계약 명세 ({cur_cases}건)</div>',
        unsafe_allow_html=True
    )
    show_cols = [c for c in ['계약일자', '제휴사', '상품구분', '상품명', '보험료', '환산1차년', '월P'] if c in df_fc_cur.columns]
    if show_cols and not df_fc_cur.empty:
        disp = df_fc_cur[show_cols].copy()
        for money_col in ['보험료', '환산1차년', '월P']:
            if money_col in disp.columns:
                disp[money_col] = disp[money_col].apply(lambda v: f"{int(v):,}원" if v else "-")
        if '계약일자' in disp.columns:
            disp['계약일자'] = disp['계약일자'].dt.strftime('%Y-%m-%d')
        st.dataframe(disp, use_container_width=True, hide_index=True)
    else:
        st.info(f"{sel_month}월 계약 데이터가 없습니다.")

    # ── 연간 전체 계약 (expander)
    with st.expander(f"📂 {sel_year}년 전체 계약 내역 ({len(df_fc_all)}건) 보기"):
        show_cols2 = [c for c in ['연', '월', '계약일자', '제휴사', '상품구분', '상품명', '보험료', '환산1차년', '월P'] if c in df_fc_all.columns]
        disp2 = df_fc_all[show_cols2].copy()
        for money_col in ['보험료', '환산1차년', '월P']:
            if money_col in disp2.columns:
                disp2[money_col] = disp2[money_col].apply(lambda v: f"{int(v):,}원" if v else "-")
        if '계약일자' in disp2.columns:
            disp2['계약일자'] = disp2['계약일자'].dt.strftime('%Y-%m-%d')
        st.dataframe(disp2.sort_values('계약일자', ascending=False) if '계약일자' in disp2 else disp2,
                     use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="text-align:center;color:#333;font-size:.72rem;margin-top:3rem;padding:1rem;
    border-top:1px solid rgba(255,255,255,0.04);">
        웰스FA · {fc_name} 상세 · 자료기준: {data_time}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
import pytz

def main():
    df_all = load_data()
    now    = datetime.datetime.now(pytz.timezone('Asia/Seoul'))

    # ── 엑셀 파일 최종 저장 시간 (한국 시간으로 변환)
    try:
        file_mtime = os.path.getmtime(DATA_FILE)
        utc_dt = datetime.datetime.fromtimestamp(file_mtime, datetime.timezone.utc)
        kst_dt = utc_dt.astimezone(pytz.timezone('Asia/Seoul'))
        data_time = kst_dt.strftime('%Y-%m-%d %H:%M')
    except Exception:
        data_time = "(시간 미확인)"

    # ── 세션 스테이트 초기화
    if 'sel_month' not in st.session_state:
        st.session_state.sel_month = now.month
    if 'sel_fc' not in st.session_state:
        st.session_state.sel_fc = None
    sel_year  = 2026
    sel_month = st.session_state.sel_month

    # ── FC 상세 페이지 분기 (이름 클릭 시 여기로)
    if st.session_state.sel_fc is not None and df_all is not None:
        # 사이드바 뒤로가기
        with st.sidebar:
            st.markdown("### ⚙️ 설정")
            st.caption(f"파일 기준 | {data_time}")
            if st.button("🏠 메인으로", key="sidebar_back"):
                st.session_state.sel_fc = None
                st.rerun()
        show_fc_detail(st.session_state.sel_fc, df_all, sel_year, sel_month, data_time)
        return

    # ── 사이드바 (모드 선택 추가)
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        view_mode = st.radio("🏠 보기 모드", ["🖥️ PC 버전", "📱 모바일 버전"], index=0)
        st.divider()
        st.caption(f"파일 기준 | {data_time}")
        if st.button("🔄 데이터 새로고침"):
            st.cache_data.clear()
            st.rerun()

    # ──────────────────────────────────────────
    # [모바일 전용 레이아웃]
    # ──────────────────────────────────────────
    if view_mode == "📱 모바일 버전":
        st.markdown(f"""
        <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:15px; border-left:4px solid #D4AF37; margin-bottom:20px;">
            <h2 style="margin:0; color:#D4AF37; font-size:1.4rem;">웰스FA 모바일 리드</h2>
            <div style="color:#8899aa; font-size:0.75rem;">기준: {data_time}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 월 선택 슬라이더 (모바일은 좌우 슬라이더가 공간 절약에 좋습니다)
        months = sorted(df_all['월'].unique().tolist()) if df_all is not None else [1]
        m_idx = months.index(sel_month) if sel_month in months else 0
        sel_month = st.select_slider("📅 분석 대상 월", options=months, value=sel_month, key="m_slider")
        if sel_month != st.session_state.get('sel_month', -1):
            st.session_state.sel_month = sel_month
        
        if df_all is None or df_all.empty:
            st.warning("📂 데이터 없음")
            return

        df = df_all[(df_all['연'] == sel_year) & (df_all['월'] == sel_month)].copy()
        
        if df.empty:
            st.info(f"📅 {sel_month}월은 아직 등록된 실적이 없습니다.")
            return

        # 모바일용 데이터 집계
        l_p = df[df['제휴사'].str.contains('생명', na=False)]['환산1차년'].sum() if '제휴사' in df.columns else 0
        l_prem = df[df['제휴사'].str.contains('생명', na=False)]['보험료'].sum() if '제휴사' in df.columns else 0
        nl_p = df[~df['제휴사'].str.contains('생명', na=False)]['보험료'].sum() if '제휴사' in df.columns else 0
        total_cases = len(df)
        active_fc = df['FC명'].nunique() if 'FC명' in df.columns else 0
        goal_rate = (l_p / 50000000 * 100)

        # 모바일용 KPI 카드 (3줄 구성)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="mobile-card"><div class="m-label">생명 환산P</div><div class="m-value">{int(l_p/10000):,}만</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mobile-card"><div class="m-label">손해 보험료</div><div class="m-value">{int(nl_p/10000):,}만</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mobile-card"><div class="m-label">목표달성</div><div class="m-value">{goal_rate:.1f}%</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="mobile-card"><div class="m-label">생명 보험료</div><div class="m-value">{int(l_prem/10000):,}만</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mobile-card"><div class="m-label">총 계약</div><div class="m-value">{total_cases:,}건</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mobile-card"><div class="m-label">활동 인원</div><div class="m-value">{active_fc}명</div></div>', unsafe_allow_html=True)
        
        # 모바일용 탭
        mt1, mt2 = st.tabs(["🏆 실적 랭킹", "📊 제휴사 통계"])
        with mt1:
            st.caption("FC 실적 순위 (월P 기준)")
            top_fc = df.groupby('FC명')['월P'].sum().sort_values(ascending=False).head(10).reset_index()
            if top_fc.empty:
                st.write("순위 데이터가 없습니다.")
            else:
                for i, row in top_fc.iterrows():
                    medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"{i+1}위"
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; padding:10px; background:rgba(255,255,255,0.02); border-radius:8px; margin-bottom:5px; border-left:2px solid #D4AF37;">
                        <span style="font-size:0.9rem;">{medal} <b>{row['FC명']}</b></span>
                        <span style="color:#D4AF37; font-weight:700;">{int(row['월P']/10000):,}만</span>
                    </div>
                    """, unsafe_allow_html=True)
        with mt2:
            st.caption("보험료 기준 제휴사별 실적 (상위 15건)")
            # 상위 15개 제휴사 추출 및 내림차순 정렬
            comp_series = df.groupby('제휴사')['보험료'].sum().sort_values(ascending=False).head(15)
            
            if comp_series.empty:
                st.write("통계 데이터가 없습니다.")
            else:
                for i, (name, val) in enumerate(comp_series.items()):
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; padding:10px; background:rgba(255,255,255,0.02); border-radius:8px; margin-bottom:5px; border-left:2px solid #667788;">
                        <span style="font-size:0.85rem; color:#ccddee;">{i+1}. {name}</span>
                        <span style="color:#f5d061; font-weight:700;">{int(val/10000):,}만</span>
                    </div>
                    """, unsafe_allow_html=True)
            
        return # 모바일 로직 종료

    # ──────────────────────────────────────────
    # [PC 버전 레이아웃] - 기존 헤더 및 월 선택
    # ──────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">🏆 웰스FA</div>
        <div class="hero-meta">WEALTH FA · PERFORMANCE BOARD · 2026</div>
        <div class="hero-badge">📂 자료기준: {data_time}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 월 선택 버튼 (1월 ~ 12월 전체 표시)
    month_cols = st.columns(12)
    for mi, mc in enumerate(month_cols):
        m = mi + 1
        with mc:
            if st.button(f"{m}월", key=f"mon_{m}", help=f"{m}월 데이터 보기", use_container_width=True):
                st.session_state.sel_month = m
                st.rerun()

    if df_all is None or df_all.empty:
        st.warning("📂 데이터 없음")
        return

    # ── 당월 / 전월 필터
    df = df_all[(df_all['연'] == sel_year) & (df_all['월'] == sel_month)].copy()
    prev_month = sel_month - 1 if sel_month > 1 else 12
    prev_year  = sel_year if sel_month > 1 else sel_year - 1
    df_prev = df_all[(df_all['연'] == prev_year) & (df_all['월'] == prev_month)].copy()

    # ──────────────────────────────────────────
    # ① HERO: MVP 리더보드 — CSS Grid 단일 블록 (Streamlit 컬럼 HTML 이슈 우회)
    # ──────────────────────────────────────────
    st.markdown(f'<div class="section-title" style="color:#D4AF37;">🏅 {sel_month}월의 MVP 현황</div>',
                unsafe_allow_html=True)

    # ── 월P Top7 데이터 준비 (콼각 = 초회 + 익월시책)
    top_p = (df.groupby('FC명')['월P'].sum()
               .sort_values(ascending=False).head(7).reset_index()
               if '월P' in df.columns and not df.empty else pd.DataFrame())

    # ── 활동 Top7 데이터 준비
    top_act = (df.groupby('FC명')['증권번호'].count()
                 .sort_values(ascending=False).head(7).reset_index()
                 .rename(columns={'증권번호':'건수'})
               if '증권번호' in df.columns and not df.empty else pd.DataFrame())

    # ── MVP 리더보드: 클릭 가능한 버튼 방식 렌더링
    # Streamlit 버튼을 HTML 패널 안에 자연스럽게 배치하기 위해
    # board-wrap 헤더는 HTML로, 각 행은 st.columns 혼합 방식 사용
    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown(
            '<div class="board-wrap">'
            '<div class="board-header" style="color:#D4AF37;">🏆 월P MVP Top 7'
            '<span style="font-size:.7rem;color:#A0A0A0;margin-left:.6rem;font-weight:400;">'
            '기준: 익월수수료 + 익월시책</span></div>',
            unsafe_allow_html=True
        )
        if top_p.empty:
            st.markdown('<p style="color:#445566;font-size:.85rem;">데이터 없음</p>', unsafe_allow_html=True)
        else:
            for i, row in top_p.iterrows():
                ic, clr, txt = p_badge(row['월P'])
                rc = rcls(i)
                is_big  = row['월P'] >= 5_000_000
                is_top3 = i < 3
                val_size = '1.3rem' if is_top3 else '1.0rem'
                rank_cls = f'mvp-rank-{i+1}' if i < 3 else 'mvp-rank-x'
                # 행 컨테이너: 순위+이름 버튼+값
                r1, r2, r3 = st.columns([1, 5, 3])
                with r1:
                    medal_html = (['🥇','🥈','🥉'][i] if i < 3 else f'<span style="color:rgba(255,255,255,0.25);font-size:.9rem;font-weight:700;">{i+1}</span>')
                    st.markdown(f'<div style="text-align:center;padding:.5rem 0;">{medal_html}</div>', unsafe_allow_html=True)
                with r2:
                    st.markdown(f'<div class="mvp-name-btn {rank_cls}"></div>', unsafe_allow_html=True)
                    if st.button(
                        row['FC명'],
                        key=f"mvp_left_{i}_{row['FC명']}",
                        help=f"👤 {row['FC명']} 님 상세 보기",
                        use_container_width=True
                    ):
                        st.session_state.sel_fc = row['FC명']
                        st.rerun()
                with r3:
                    st.markdown(f'<div style="color:{clr};font-size:{val_size};text-align:right;font-weight:900;padding:.4rem 0;white-space:nowrap;">{ic} {txt}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown(
            '<div class="board-wrap">'
            '<div class="board-header" style="color:#FF6B6B;">🔥 활동 MVP Top 7'
            '<span style="font-size:.72rem;color:#556677;margin-left:.5rem;">이달 계약 건수</span></div>',
            unsafe_allow_html=True
        )
        if top_act.empty:
            st.markdown('<p style="color:#445566;font-size:.85rem;">데이터 없음</p>', unsafe_allow_html=True)
        else:
            for i, row in top_act.iterrows():
                rank_cls = f'mvp-rank-{i+1}' if i < 3 else 'mvp-rank-x'
                r1, r2, r3 = st.columns([1, 5, 3])
                with r1:
                    medal_html = (['🥇','🥈','🥉'][i] if i < 3 else f'<span style="color:rgba(255,255,255,0.25);font-size:.9rem;font-weight:700;">{i+1}</span>')
                    st.markdown(f'<div style="text-align:center;padding:.5rem 0;">{medal_html}</div>', unsafe_allow_html=True)
                with r2:
                    st.markdown(f'<div class="mvp-name-btn {rank_cls}"></div>', unsafe_allow_html=True)
                    if st.button(
                        row['FC명'],
                        key=f"mvp_right_{i}_{row['FC명']}",
                        help=f"👤 {row['FC명']} 님 상세 보기",
                        use_container_width=True
                    ):
                        st.session_state.sel_fc = row['FC명']
                        st.rerun()
                with r3:
                    cnt_color = '#FF6B6B' if i < 3 else '#DD5555'
                    st.markdown(f'<div style="color:{cnt_color};font-size:1.3rem;font-weight:900;text-align:right;padding:.4rem 0;">{int(row["건수"])}<span style="font-size:.7rem;font-weight:500;">건</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # ② KPI 5종 — 생명/손해 분리
    # ──────────────────────────────────────────

    # ── 생명 / 손해 구분: 제휴사(col[3]) 이름에 '생명' 포함 여부
    # 삼성생명, 미래에셋생명, 농협생명 → 생명보험
    # 그 외 (DB손해, 현대해상, KB손해 등) → 손해보험
    if '제휴사' in df.columns:
        mask_life = df['제휴사'].astype(str).str.contains('생명', na=False)
    else:
        # 폴백: 제휴사 컬럼 없으면 상품구분으로 대체
        mask_life = df['상품구분'].astype(str).str.contains('생명', na=False)
    df_life  = df[mask_life]
    df_nhic  = df[~mask_life]

    # ── 집계
    life_premium  = df_life['보험료'].sum()     if '보험료'   in df_life.columns and not df_life.empty else 0
    life_환산    = df_life['환산1차년'].sum() if '환산1차년' in df_life.columns and not df_life.empty else 0  # 보험사환산_1차년
    nhic_premium  = df_nhic['보험료'].sum()     if '보험료'   in df_nhic.columns and not df_nhic.empty else 0
    total_cases   = len(df)
    active_fc     = df['FC명'].nunique()  if 'FC명' in df.columns else 0

    # ── 전월 대비 (총 건수)
    prev_cases = len(df_prev)
    def delta(cur, prev):
        if prev == 0: return "—"
        d = (cur - prev) / prev * 100
        arrow = "▲" if d >= 0 else "▼"
        return f"{arrow} {abs(d):.1f}% (전월比)"

    kpis = [
        ("🏦", "생명보험 총월납",   f"{int(life_premium/10000):,}만",   "생명보험사 월납 보험료"),
        ("💎", "생명보험 환산",     f"{int(life_환산/10000):,}만",   "보험사환산_1차년 합계"),
        ("🛡️", "손해보험 총월납",   f"{int(nhic_premium/10000):,}만",   "손해보험사 월납 보험료"),
        ("📋", "생손보 총계약건수", f"{total_cases:,}건",               delta(total_cases, prev_cases)),
        ("👥", "활동 FC",          f"{active_fc}명",                   f"{sel_month}월 계약 존재 FC"),
    ]

    cols_kpi = st.columns(5)
    for col, (ico, lbl, val, sub) in zip(cols_kpi, kpis):
        with col:
            sub_color = ("#D4AF37" if "▲" in sub
                         else "#FF6B6B" if "▼" in sub
                         else "#606060")
            st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-icon">{ico}</div>
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-val">{val}</div>
                <div class="kpi-sub" style="color:{sub_color};">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # ③ 팀 목표 달성률 — 제휴사별 그래픽
    # ──────────────────────────────────────────
    st.markdown('<div class="section-title" style="color:#88ccff;">🏢 제휴사별 현황</div>',
                unsafe_allow_html=True)

    # ── 제휴사별 집계
    has_insurer  = '제휴사' in df.columns
    has_hwan     = '환산1차년' in df.columns
    has_premium  = '보험료' in df.columns

    if has_insurer and (has_hwan or has_premium):
        # 제휴사별 그룹
        grp_cols = {'제휴사': []}
        if has_hwan:    grp_cols['환산1차년'] = 'sum'
        if has_premium: grp_cols['보험료']    = 'sum'
        grp_cols['계약'] = 'count'

        agg_dict = {}
        if has_hwan:    agg_dict['환산1차년'] = 'sum'
        if has_premium: agg_dict['보험료']    = 'sum'
        agg_dict['FC명'] = 'count'   # 계약건수 대리

        df_grp = (df.groupby('제휴사')
                    .agg(agg_dict)
                    .reset_index()
                    .rename(columns={'FC명': '계약건수'}))

        # 생명/손해 분류
        df_grp['구분'] = df_grp['제휴사'].apply(
            lambda x: '생명' if '생명' in str(x) else '손해'
        )
        df_life_grp = df_grp[df_grp['구분'] == '생명'].copy()
        df_nhic_grp = df_grp[df_grp['구분'] == '손해'].copy()

        # ── 좌(생명) / 우(손해) 2열 분할 — 클릭 없이 한눈에!
        col_life, col_nhic = st.columns([1, 1], gap="large")

        # ════════════════════════════
        # 왼쪽: 생명보험사
        # ════════════════════════════
        with col_life:
            st.markdown(
                '<div style="color:#D4AF37;font-size:1rem;font-weight:800;'
                'border-bottom:1px solid rgba(212,175,55,0.3);padding-bottom:0.4rem;'
                'margin-bottom:0.8rem;">🏦 생명보험사</div>',
                unsafe_allow_html=True
            )
            if df_life_grp.empty:
                st.info("이달 생명보험 계약 없음")
            else:
                insurers_life = df_life_grp['제휴사'].tolist()
                bar_h = max(180, len(insurers_life) * 55)

                # ─ 보험사환산 차트
                if has_hwan:
                    st.markdown(
                        '<div style="color:#A88820;font-size:0.78rem;'
                        'letter-spacing:1px;margin-bottom:0.3rem;">💎 보험사환산 (1차년)</div>',
                        unsafe_allow_html=True
                    )
                    fig_hwan = go.Figure()
                    for _, row_g in df_life_grp.iterrows():
                        val = row_g['환산1차년']
                        pct = val / MONTHLY_GOAL_P * 100 if MONTHLY_GOAL_P else 0
                        clr = '#D4AF37' if pct >= 100 else ('#E8A020' if pct >= 60 else '#8B5E10')
                        fig_hwan.add_trace(go.Bar(
                            x=[val], y=[row_g['제휴사']], orientation='h',
                            marker=dict(color=clr, line=dict(color='rgba(212,175,55,0.3)', width=1)),
                            text=f" {int(val/10000):,}만 ({pct:.0f}%)",
                            textposition='outside',
                            textfont=dict(color='#C8A030', size=11),
                            hovertemplate=f"<b>{row_g['제휴사']}</b><br>환산: {int(val/10000):,}만<br>달성률: {pct:.1f}%<extra></extra>"
                        ))
                    fig_hwan.add_vline(
                        x=MONTHLY_GOAL_P, line_dash="dash",
                        line_color="rgba(212,175,55,0.4)",
                        annotation_text=f"목표 {int(MONTHLY_GOAL_P/10000):,}만",
                        annotation_font=dict(color="#D4AF37", size=10),
                        annotation_position="top right"
                    )
                    fig_hwan.update_layout(
                        showlegend=False, height=bar_h,
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=70, t=10, b=10),
                        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                                   tickfont=dict(color='#606060', size=9), tickformat=','),
                        yaxis=dict(tickfont=dict(color='#D4B870', size=12)),
                        bargap=0.3,
                    )
                    st.plotly_chart(fig_hwan, use_container_width=True)

                # ─ 보험료 차트
                if has_premium:
                    st.markdown(
                        '<div style="color:#4A9090;font-size:0.78rem;'
                        'letter-spacing:1px;margin-bottom:0.3rem;margin-top:0.5rem;">🏦 월납 보험료</div>',
                        unsafe_allow_html=True
                    )
                    fig_prem = go.Figure()
                    for _, row_g in df_life_grp.iterrows():
                        val = row_g['보험료']
                        fig_prem.add_trace(go.Bar(
                            x=[val], y=[row_g['제휴사']], orientation='h',
                            marker=dict(color='#4A9090', line=dict(color='rgba(74,144,144,0.3)', width=1)),
                            text=f" {int(val/10000):,}만",
                            textposition='outside',
                            textfont=dict(color='#60B0B0', size=11),
                            hovertemplate=f"<b>{row_g['제휴사']}</b><br>보험료: {int(val/10000):,}만<extra></extra>"
                        ))
                    fig_prem.update_layout(
                        showlegend=False, height=bar_h,
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=70, t=10, b=10),
                        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                                   tickfont=dict(color='#606060', size=9), tickformat=','),
                        yaxis=dict(tickfont=dict(color='#80C8C8', size=12)),
                        bargap=0.3,
                    )
                    st.plotly_chart(fig_prem, use_container_width=True)

                # ─ 생명 요약 테이블
                import pandas as _pd
                summary_life = []
                for _, row_g in df_life_grp.iterrows():
                    summary_life.append({
                        '제휴사':     row_g['제휴사'],
                        '환산(만)':   f"{int(row_g.get('환산1차년',0)/10000):,}" if has_hwan else '-',
                        '보험료(만)': f"{int(row_g.get('보험료',0)/10000):,}" if has_premium else '-',
                        '건수':       f"{int(row_g.get('계약건수',0))}건",
                    })
                st.dataframe(_pd.DataFrame(summary_life), use_container_width=True, hide_index=True)

        # ════════════════════════════
        # 오른쪽: 손해보험사
        # ════════════════════════════
        with col_nhic:
            st.markdown(
                '<div style="color:#FF6B6B;font-size:1rem;font-weight:800;'
                'border-bottom:1px solid rgba(255,107,107,0.3);padding-bottom:0.4rem;'
                'margin-bottom:0.8rem;">🛡️ 손해보험사</div>',
                unsafe_allow_html=True
            )
            if df_nhic_grp.empty:
                st.info("이달 손해보험 계약 없음")
            else:
                insurers_nhic = df_nhic_grp['제휴사'].tolist()
                bar_h2 = max(180, len(insurers_nhic) * 55)

                # ─ 보험료 차트
                if has_premium:
                    st.markdown(
                        '<div style="color:#AA4444;font-size:0.78rem;'
                        'letter-spacing:1px;margin-bottom:0.3rem;">🛡️ 월납 보험료</div>',
                        unsafe_allow_html=True
                    )
                    # 순위별 색상 그라디언트
                    nhic_sorted = df_nhic_grp.sort_values('보험료', ascending=False).reset_index(drop=True)
                    red_palette = ['#FF6B6B','#EE5555','#DD4444','#CC3333','#BB2222','#AA1111']
                    fig_nhic = go.Figure()
                    for idx, row_g in nhic_sorted.iterrows():
                        val = row_g['보험료']
                        clr = red_palette[min(idx, len(red_palette)-1)]
                        fig_nhic.add_trace(go.Bar(
                            x=[val], y=[row_g['제휴사']], orientation='h',
                            marker=dict(color=clr, line=dict(color='rgba(255,107,107,0.3)', width=1)),
                            text=f" {int(val/10000):,}만",
                            textposition='outside',
                            textfont=dict(color='#FF8888', size=11),
                            hovertemplate=f"<b>{row_g['제휴사']}</b><br>보험료: {int(val/10000):,}만<extra></extra>"
                        ))
                    fig_nhic.update_layout(
                        showlegend=False, height=bar_h2,
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=70, t=10, b=10),
                        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                                   tickfont=dict(color='#606060', size=9), tickformat=','),
                        yaxis=dict(tickfont=dict(color='#FF9999', size=12)),
                        bargap=0.3,
                    )
                    st.plotly_chart(fig_nhic, use_container_width=True)

                # ─ 손해 요약 테이블
                summary_nhic_rows = []
                for _, row_g in df_nhic_grp.iterrows():
                    summary_nhic_rows.append({
                        '제휴사':     row_g['제휴사'],
                        '보험료(만)': f"{int(row_g.get('보험료',0)/10000):,}" if has_premium else '-',
                        '건수':       f"{int(row_g.get('계약건수',0))}건",
                    })
                st.dataframe(_pd.DataFrame(summary_nhic_rows), use_container_width=True, hide_index=True)

    else:
        # 폴백: 제휴사 컬럼 없을 때 기존 프로그레스바
        g1, g2 = st.columns(2, gap="large")
        with g1:
            pct_p = min(life_환산 / MONTHLY_GOAL_P * 100, 100) if MONTHLY_GOAL_P else 0
            st.markdown(f"""
            <div class="chart-box">
                <div style="margin-bottom:1rem;">
                    <span style="color:#D4AF37;font-weight:700;">생명보험 환산 달성률</span>
                    <span style="float:right;color:#D4AF37;font-weight:900;font-size:1.3rem;">{pct_p:.1f}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" style="width:{pct_p}%;"></div></div>
                <div style="margin-top:.6rem;font-size:.75rem;color:#606060;">
                    달성: {int(life_환산/10000):,}만 / 목표: {int(MONTHLY_GOAL_P/10000):,}만
                </div>
            </div>
            """, unsafe_allow_html=True)
        with g2:
            pct_c = min(total_cases / MONTHLY_GOAL_CASES * 100, 100) if MONTHLY_GOAL_CASES else 0
            st.markdown(f"""
            <div class="chart-box">
                <div style="margin-bottom:1rem;">
                    <span style="color:#FF6B6B;font-weight:700;">계약건수 달성률</span>
                    <span style="float:right;color:#FF6B6B;font-weight:900;font-size:1.3rem;">{pct_c:.1f}%</span>
                </div>
                <div class="prog-bar"><div class="prog-fill" style="width:{pct_c}%;background:linear-gradient(90deg,#551122,#FF6B6B);"></div></div>
                <div style="margin-top:.6rem;font-size:.75rem;color:#606060;">
                    달성: {total_cases:,}건 / 목표: {MONTHLY_GOAL_CASES:,}건
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # ③ 최근 업데이트된 계약 (15건) 
    # ──────────────────────────────────────────
    st.markdown('<div class="section-title" style="color:#D4AF37;">📝 최근 업데이트 계약</div>', 
                unsafe_allow_html=True)
    
    # 엑셀의 가장 아래쪽(최근 입력) 데이터 15개 추출
    if df_all is not None and not df_all.empty:
        latest_15 = df_all.iloc[::-1].head(15).copy()
        
        # 가공: 날짜 포맷 및 보험료 등 만단위 표시
        latest_15['일자'] = latest_15['계약일자'].dt.strftime('%Y-%m-%d')
        latest_15['보험료(만)'] = latest_15['보험료'].apply(lambda x: f"{int(x/10000):,}만")
        latest_15['익월P(만)'] = latest_15['익월P'].apply(lambda x: f"{int(x/10000):,}만")
        latest_15['시책(만)'] = latest_15['익월시책'].apply(lambda x: f"{int(x/10000):,}만")
        
        # 보여줄 컬럼만 선택 및 이름 변경
        display_latest = latest_15[['일자', 'FC명', '제휴사', '상품명', '보험료(만)', '납입기간', '익월P(만)', '시책(만)']]
        display_latest.columns = ['계약일자', '담당FC', '제휴사', '상품명', '보험료', '납입기간', '익월P', '익월시책']
        
        st.markdown('<div class="glass-panel" style="padding:10px; margin-bottom:20px;">', unsafe_allow_html=True)
        st.dataframe(
            display_latest,
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("표시할 최근 계약 데이터가 없습니다.")

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)



    # ──────────────────────────────────────────
    # ④ 통합 리더보드 (확정 시안)
    # ──────────────────────────────────────────
    st.markdown('<div class="section-title" style="color:#88ccff;">🥇 활동 FC 통합 리더보드</div>',
                unsafe_allow_html=True)
    
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    if '월P' in df.columns and not df.empty:
        # 데이터 집계 (월P 기준)
        lead_df = df.groupby('FC명').agg({
            '월P': 'sum',
            '보험료': 'sum'
        }).reset_index()
        # 건수 추가
        cnt_df = df.groupby('FC명')['증권번호'].count().reset_index().rename(columns={'증권번호':'건수'})
        lead_df = _pd.merge(lead_df, cnt_df, on='FC명')
        
        # 전체 정렬 (월P 기준 상향 정렬 - Plotly 가로막대는 아래서 위로 그려짐)
        lead_df = lead_df.sort_values('월P', ascending=True)
        total_fc_count = len(lead_df)

        def get_rank_label(idx, total):
            rank = total - idx
            if rank == 1: return "🥇 1위"
            if rank == 2: return "🥈 2위"
            if rank == 3: return "🥉 3위"
            return f"{rank}위"

        fig_lead = go.Figure()
        for i, row in lead_df.reset_index(drop=True).iterrows():
            rank_label = get_rank_label(i, total_fc_count)
            # 환산P는 툴팁으로만 보여줄 수 있게 처리 (필요시)
            fig_lead.add_trace(go.Bar(
                x=[row['월P']], y=[row['FC명']],
                orientation='h', name=row['FC명'],
                marker=dict(color=row['월P'], colorscale='YlOrBr', 
                            line=dict(color='rgba(212,175,55,0.3)', width=1)),
                text=f" {rank_label} | {int(row['월P']/10000):,}만 | {row['건수']}건",
                textposition='outside', textfont=dict(color='#D4AF37', size=12),
                hovertemplate=(f"<b>{row['FC명']}</b><br>월P 성과: {int(row['월P']/10000):,}만<br>"
                               f"총보험료: {int(row['보험료']/10000):,}만<br>계약건수: {row['건수']}건<extra></extra>")
            ))
        
        # 인원수에 따른 스케일링 높이 계산 (1인당 40px + 기본 여백 100px)
        dynamic_height = max(450, total_fc_count * 42)
        
        fig_lead.update_layout(**PLOTLY_LAYOUT)
        fig_lead.update_layout(
            height=dynamic_height,
            showlegend=False, margin=dict(l=10, r=130, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', tickformat=','),
            yaxis=dict(tickfont=dict(color='#aabbcc', size=12)), bargap=0.3
        )
        st.plotly_chart(fig_lead, use_container_width=True)
        st.caption(f"💡 현재 총 {total_fc_count}명의 활동 FC 정보를 월P 성과순으로 표시하고 있습니다.")
    else:
        st.info("실적 데이터가 없습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)



    # ──────────────────────────────────────────
    # ⑤ 제휴사별 연간 성장 추이 (Line Trend)
    # ──────────────────────────────────────────
    st.markdown('<div class="section-title" style="color:#88ccff;">📈 2026 연간 제휴사별 실적 트렌드</div>',
                unsafe_allow_html=True)
    
    if df_all is not None and not df_all.empty:
        # 연간 데이터 준비
        annual_raw = df_all[df_all['연'] == sel_year].copy()
        
        # 제휴사 구분 로직
        mask_life = annual_raw['제휴사'].astype(str).str.contains('생명', na=False)
        df_annual_life = annual_raw[mask_life]
        df_annual_nhic = annual_raw[~mask_life]

        # 상단 탭 구성
        trend_tab1, trend_tab2 = st.tabs(["💸 손해보험 (보험료)", "🏥 생명보험 (환산/보험료)"])

        # 🅐 손해보험 섹션
        with trend_tab1:
            if not df_annual_nhic.empty:
                nhic_grp = df_annual_nhic.groupby(['월', '제휴사'])['보험료'].sum().reset_index()
                fig_nhic = px.line(
                    nhic_grp, x="월", y="보험료", color="제휴사",
                    markers=True, template="plotly_dark",
                    category_orders={"월": list(range(1, 13))},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_nhic.update_layout(**PLOTLY_LAYOUT)
                fig_nhic.update_layout(
                    height=400, margin=dict(l=10, r=10, t=30, b=50),
                    xaxis=dict(tickvals=list(range(1, 13)), ticktext=[f"{m}월" for m in range(1, 13)]),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.03)', tickformat=',')
                )
                st.plotly_chart(fig_nhic, use_container_width=True)
            else:
                st.info("손해보험 데이터가 없습니다.")

        # 🅑 생명보험 섹션
        with trend_tab2:
            if not df_annual_life.empty:
                # 메트릭 선택 라디오
                m_col1, m_col2 = st.columns([3, 7])
                with m_col1:
                    target_metric = st.radio("분석 지표 선택", ["환산1차년", "보험료"], horizontal=True, key="life_metric")
                
                life_grp = df_annual_life.groupby(['월', '제휴사'])[target_metric].sum().reset_index()
                fig_life = px.line(
                    life_grp, x="월", y=target_metric, color="제휴사",
                    markers=True, template="plotly_dark",
                    category_orders={"월": list(range(1, 13))},
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig_life.update_layout(**PLOTLY_LAYOUT)
                fig_life.update_layout(
                    height=400, margin=dict(l=10, r=10, t=30, b=50),
                    xaxis=dict(tickvals=list(range(1, 13)), ticktext=[f"{m}월" for m in range(1, 13)]),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.03)', tickformat=',')
                )
                st.plotly_chart(fig_life, use_container_width=True)
            else:
                st.info("생명보험 데이터가 없습니다.")
        
        st.caption("💡 상단 범례를 클릭하면 특정 회사만 집중적으로 비교할 수 있습니다 (더블클릭 시 해당 회사만 보기).")
    else:
        st.info("실적 데이터가 존재하지 않습니다.")

    st.markdown('<hr class="fancy">', unsafe_allow_html=True)


    # ──────────────────────────────────────────
    # ⑥ FC 빠른 조회 (selectbox — 메인 페이지 내)
    # ──────────────────────────────────────────
    st.markdown('<hr class="fancy">', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="color:#88ccff;">🔍 FC 개인 실적 바로가기</div>',
                unsafe_allow_html=True)
    all_fcs = sorted(df_all['FC명'].dropna().unique().tolist()) if df_all is not None else []
    col_sel, col_go = st.columns([5, 1])
    with col_sel:
        chosen = st.selectbox("👤 FC 선택 후 → 버튼 클릭", [""] + all_fcs,
                              key="quick_fc_sel", label_visibility="collapsed")
    with col_go:
        if st.button("상세 보기 →", use_container_width=True, key="quick_go_btn"):
            if chosen:
                st.session_state.sel_fc = chosen
                st.rerun()

    # ──────────────────────────────────────────
    # ⑦ 원본 데이터
    # ──────────────────────────────────────────
    with st.expander("📂 원본 RAWDATA 보기 (클릭하여 펼치기)"):
        show_cols = [c for c in ['FC명','직급','증권번호','상품구분','상품명','보험료','환산1차년','계약일자']
                     if c in df.columns]
        st.dataframe(df[show_cols] if show_cols else df,
                     use_container_width=True, hide_index=True)

    # 푸터
    st.markdown(f"""
    <div style="text-align:center;color:#333;font-size:.72rem;margin-top:3rem;padding:1rem;
    border-top:1px solid rgba(255,255,255,0.04);">
        웰스FA · 데이터: 26년종합.xlsx (RAWDATA) · 자료기준: {data_time}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
