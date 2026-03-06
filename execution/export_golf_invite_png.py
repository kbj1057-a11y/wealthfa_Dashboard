"""
Golf Tournament HTML → PNG 이미지 변환
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE     = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.abspath(os.path.join(BASE, "..", "매일업데이트", "Golf_Tournament_Invite.html"))
OUT_PATH  = os.path.abspath(os.path.join(BASE, "..", "매일업데이트", "Golf_Tournament_Invite.png"))

print("=" * 50)
print("  Golf Invite HTML → PNG 변환")
print("=" * 50)
print(f"  HTML: {os.path.basename(HTML_PATH)}")

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ playwright 없음.")
    sys.exit(1)

SCALE = 3   # 3배 고해상도 (1350×2400px) — 4로 변경시 최고화질

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 450, "height": 800},
        device_scale_factor=SCALE,   # ← 핵심: 3배율 고해상도
    )
    page = context.new_page()

    url = "file:///" + HTML_PATH.replace("\\", "/")
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(1500)  # 폰트/애니메이션 로드 대기

    # .poster 요소만 캡처
    poster = page.locator(".poster")
    poster.screenshot(path=OUT_PATH, type="png")

    browser.close()

if os.path.exists(OUT_PATH):
    size_kb = os.path.getsize(OUT_PATH) / 1024
    print(f"✅ PNG 저장 완료! ({size_kb:.0f} KB)")
    print(f"  📂 {OUT_PATH}")
    import subprocess
    subprocess.Popen(f'explorer /select,"{OUT_PATH}"')
else:
    print("❌ 저장 실패")
