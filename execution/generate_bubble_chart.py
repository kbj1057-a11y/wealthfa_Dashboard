"""
웰스FA - 성과 버블 성장 차트 생성기
2/1 ~ 오늘까지 FC별 누적 실적이 버블로 성장하는 애니메이션
"""
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os, sys

# 출력 인코딩
sys.stdout.reconfigure(encoding='utf-8')

# ── 경로 설정
BASE     = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "..", "매일업데이트", "flourish_race_daily.csv")
OUT_PATH = os.path.join(BASE, "..", "매일업데이트", "bubble_growth.html")

# ── 다크 골드 컬러 팔레트 (FC별 고유 색상)
COLORS = [
    "#D4AF37","#F5D061","#E8A020","#C68B2F","#FFE082",
    "#81C784","#64B5F6","#F48FB1","#CE93D8","#80DEEA",
    "#FFAB91","#A5D6A7","#90CAF9","#F48FB1","#B0BEC5",
    "#FFD54F","#4DB6AC","#7986CB","#FF8A65","#9CCC65",
    "#26C6DA","#EC407A","#AB47BC","#42A5F5","#66BB6A",
    "#FFA726","#26A69A","#5C6BC0","#EF5350","#8D6E63",
    "#78909C","#BDBDBD","#F06292","#AED581","#4DD0E1",
]

def arrange_bubbles(n):
    """FC들을 원형 + 내부 배치 (경쟁감 없는 레이아웃)"""
    positions = []
    # 황금비 나선 배치
    golden_ratio = (1 + np.sqrt(5)) / 2
    for i in range(n):
        theta = 2 * np.pi * i / golden_ratio
        r = np.sqrt(i / n) * 4.5
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        positions.append((round(x, 3), round(y, 3)))
    return positions

def main():
    # 1. 데이터 로드
    if not os.path.exists(CSV_PATH):
        print(f"오류: CSV 파일이 없습니다.\n  경로: {CSV_PATH}")
        print("  먼저 generate_race_data.py 를 실행하세요!")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH, index_col=0, encoding='utf-8-sig')
    fc_names = df.index.tolist()
    dates    = df.columns.tolist()
    n_fc     = len(fc_names)

    print(f"FC 수: {n_fc}명 / 날짜: {dates[0]} ~ {dates[-1]} ({len(dates)}일)")

    # 2. 버블 위치 계산 (고정)
    positions = arrange_bubbles(n_fc)
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]

    # 3. 최대 실적 (버블 크기 스케일링용)
    max_val = df.max().max()
    if max_val == 0:
        max_val = 1

    # 4. 각 날짜별 프레임 생성
    frames = []
    for date in dates:
        vals = df[date].tolist()

        # 버블 크기: 최대 버블 대비 상대 크기 (최소 8, 최대 80)
        sizes = [max(10, (v / max_val) * 90) for v in vals]

        # 툴팁 텍스트
        texts = [
            f"<b>{name}</b><br>{date}<br>누적 실적: {int(v):,}원"
            for name, v in zip(fc_names, vals)
        ]

        frame = go.Frame(
            name=date,
            data=[go.Scatter(
                x=xs, y=ys,
                mode="markers+text",
                marker=dict(
                    size=sizes,
                    sizemode="diameter",
                    color=[COLORS[i % len(COLORS)] for i in range(n_fc)],
                    opacity=0.82,
                    line=dict(width=1.5, color="rgba(255,255,255,0.3)"),
                ),
                text=[name.split(" ")[-1] if " " in name else name[:2] for name in fc_names],
                textposition="middle center",
                textfont=dict(
                    color="rgba(0,0,0,0.85)",
                    size=10,
                    family="Noto Sans KR, sans-serif"
                ),
                hovertext=texts,
                hoverinfo="text",
                customdata=vals,
            )]
        )
        frames.append(frame)

    # 5. 초기 데이터 (첫 날짜)
    first_date = dates[0]
    init_vals  = df[first_date].tolist()
    init_sizes = [max(10, (v / max_val) * 90) for v in init_vals]
    init_texts = [
        f"<b>{name}</b><br>{first_date}<br>누적 실적: {int(v):,}원"
        for name, v in zip(fc_names, init_vals)
    ]

    # 6. 슬라이더 스텝
    sliders = [{
        "active": 0,
        "currentvalue": {"prefix": "📅 ", "font": {"color": "#D4AF37", "size": 14}},
        "pad": {"b": 10, "t": 60},
        "bgcolor": "rgba(30,25,10,0.8)",
        "bordercolor": "rgba(212,175,55,0.3)",
        "steps": [
            {
                "args": [[date], {"frame": {"duration": 400, "redraw": True}, "mode": "immediate"}],
                "label": date,
                "method": "animate"
            }
            for date in dates
        ]
    }]

    # 7. 레이아웃
    layout = go.Layout(
        title=dict(
            text="🌟 웰스FA · 성과 버블 성장 차트 · 2026",
            font=dict(color="#D4AF37", size=22, family="Noto Sans KR, sans-serif"),
            x=0.5, xanchor="center", y=0.97
        ),
        paper_bgcolor="#0D0D0D",
        plot_bgcolor="#111111",
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-6, 6]
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-6, 6]
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=100),
        height=700,
        font=dict(family="Noto Sans KR, sans-serif"),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 0,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "bgcolor": "rgba(212,175,55,0.15)",
            "bordercolor": "rgba(212,175,55,0.5)",
            "font": {"color": "#D4AF37"},
            "buttons": [
                {
                    "label": "▶ 재생",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 500, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 300, "easing": "quadratic-in-out"}
                    }]
                },
                {
                    "label": "⏸ 정지",
                    "method": "animate",
                    "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]
                }
            ]
        }],
        sliders=sliders,
        annotations=[
            dict(
                text="버블 크기 = 누적 실적(월P) | 색상 = FC별 고유 컬러",
                x=0.5, y=-0.08, xref="paper", yref="paper",
                showarrow=False,
                font=dict(color="rgba(180,160,80,0.6)", size=11)
            )
        ]
    )

    # 8. 초기 트레이스
    init_trace = go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        marker=dict(
            size=init_sizes,
            sizemode="diameter",
            color=[COLORS[i % len(COLORS)] for i in range(n_fc)],
            opacity=0.82,
            line=dict(width=1.5, color="rgba(255,255,255,0.3)"),
        ),
        text=[name.split(" ")[-1] if " " in name else name[:2] for name in fc_names],
        textposition="middle center",
        textfont=dict(color="rgba(0,0,0,0.85)", size=10, family="Noto Sans KR, sans-serif"),
        hovertext=init_texts,
        hoverinfo="text",
    )

    fig = go.Figure(data=[init_trace], layout=layout, frames=frames)

    # 9. HTML 저장
    fig.write_html(
        OUT_PATH,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False}
    )

    print(f"SUCCESS: {OUT_PATH}")
    print("브라우저로 열어 재생 버튼을 누르세요!")

if __name__ == "__main__":
    main()
