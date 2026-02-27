"""
웰스FA 별자리 타임랩스 → 자동 동영상 녹화 (Playwright)
- 재생속도: 느리게 (1200ms/프레임)
- 타이밍: JS 완료 신호(window.ANIM_DONE) 감지 방식으로 정확히 종료
"""
import os, sys, time, glob, shutil, subprocess, datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE      = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.abspath(os.path.join(BASE, "..", "매일업데이트", "constellation_timelapse.html"))
OUT_DIR   = os.path.abspath(os.path.join(BASE, "..", "매일업데이트"))

# ── 최대 대기 시간 (느리게 기준 안전값)
# 느리게(1200ms) × 25프레임 + 피날레(7×2.2s) + 초기/버퍼
# = 30s + 15.4s + 2s + 20s(넉넉한버퍼) = ~68초
MAX_WAIT_SEC   = 90    # 최대 90초까지 기다림 (그 전에 ANIM_DONE 감지하면 즉시 종료)
POLL_INTERVAL  = 0.8   # 0.8초마다 완료 여부 확인

print("=" * 55)
print("  웰스FA 별자리 · 자동 동영상 녹화")
print("  재생속도: 느리게 (1200ms/프레임)")
print("=" * 55)
print(f"  HTML: {os.path.basename(HTML_PATH)}")
print(f"  최대 대기: {MAX_WAIT_SEC}초 (완료 신호 감지 시 즉시 종료)")
print()

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ playwright가 설치되어 있지 않습니다.")
    sys.exit(1)

def record():
    now_str  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    webm_dir = os.path.join(OUT_DIR, "_video_tmp")
    os.makedirs(webm_dir, exist_ok=True)

    print("🎬 브라우저 열고 녹화 시작...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--disable-infobars"]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=webm_dir,
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        url = "file:///" + HTML_PATH.replace("\\", "/")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)

        print(f"⏱️  애니메이션 재생 중... (완료 신호 대기, 최대 {MAX_WAIT_SEC}초)")
        print()

        # ── window.ANIM_DONE 신호 폴링으로 정확한 종료 감지
        start_time  = time.time()
        done        = False
        bar_len     = 40

        for tick in range(int(MAX_WAIT_SEC / POLL_INTERVAL)):
            page.wait_for_timeout(int(POLL_INTERVAL * 1000))
            elapsed = time.time() - start_time
            remain  = max(0, MAX_WAIT_SEC - elapsed)

            # 완료 신호 확인
            try:
                anim_done = page.evaluate("window.ANIM_DONE")
            except Exception:
                anim_done = False

            # 진행 바 표시
            ratio  = min(elapsed / MAX_WAIT_SEC, 1.0)
            filled = int(bar_len * ratio)
            bar    = "█" * filled + "░" * (bar_len - filled)
            status = "✅ 완료!" if anim_done else f"남은 시간: {int(remain)}초"
            print(f"\r  [{bar}] {int(elapsed):3d}초 | {status}   ", end="", flush=True)

            if anim_done:
                # 피날레 완료 후 약간의 여운(2초) 더 녹화 후 종료
                print()
                print("\n🎬 피날레 완료! 2초 여운 녹화 후 저장...")
                page.wait_for_timeout(2000)
                done = True
                break

        if not done:
            print()
            print(f"\n⏰ 최대 대기 시간({MAX_WAIT_SEC}초) 도달, 강제 종료")

        print("✅ 녹화 완료! 파일 저장 중...")
        context.close()   # 여기서 webm 저장
        browser.close()

    # ── webm 파일 찾기 & 이름 변경
    webm_files = sorted(glob.glob(os.path.join(webm_dir, "*.webm")),
                        key=os.path.getmtime, reverse=True)
    if not webm_files:
        print("❌ 녹화 파일을 찾을 수 없습니다.")
        return None

    src_webm  = webm_files[0]
    dest_webm = os.path.join(OUT_DIR, f"별자리_타임랩스_{now_str}.webm")
    shutil.move(src_webm, dest_webm)
    try:
        shutil.rmtree(webm_dir)
    except Exception:
        pass

    print(f"📁 WebM 저장: {dest_webm}")
    return dest_webm

def try_convert_mp4(webm_path):
    """moviepy로 WebM → MP4 변환 (별도 ffmpeg 설치 불필요)"""
    mp4_path = webm_path.replace(".webm", ".mp4")
    print()
    print("🔄 MP4 변환 중... (잠시만 기다려주세요)")

    try:
        from moviepy import VideoFileClip
        clip = VideoFileClip(webm_path)
        duration = round(clip.duration, 1)
        print(f"   영상 길이: {duration}초 / 해상도: {clip.size[0]}×{clip.size[1]}")
        clip.write_videofile(
            mp4_path,
            codec="libx264",
            fps=24,
            preset="fast",
            audio=False,
            logger="bar"
        )
        clip.close()

        if os.path.exists(mp4_path):
            size_mb = os.path.getsize(mp4_path) / (1024 * 1024)
            print(f"✅ MP4 저장 완료! ({size_mb:.1f} MB)")
            os.remove(webm_path)   # 원본 webm 삭제
            return mp4_path

    except ImportError:
        print("⚠️  moviepy 없음. 설치 중...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "moviepy", "-q"],
            check=True
        )
        print("   재시도 중...")
        return try_convert_mp4(webm_path)   # 재귀 재시도

    except Exception as e:
        print(f"⚠️  변환 실패: {e}")
        print(f"   WebM 파일은 그대로 유지됩니다: {webm_path}")

    return None


def main():
    if not os.path.exists(HTML_PATH):
        print(f"❌ HTML 파일 없음: {HTML_PATH}")
        print("   먼저 export_timelapse_html.py를 실행하세요.")
        sys.exit(1)

    webm_path  = record()
    if not webm_path:
        sys.exit(1)

    mp4_path   = try_convert_mp4(webm_path)
    final_path = mp4_path or webm_path

    print()
    print("=" * 55)
    print("  🎉 동영상 생성 완료!")
    print(f"  📂 파일: {os.path.basename(final_path)}")
    print(f"  📁 폴더: {os.path.dirname(final_path)}")
    print("=" * 55)
    subprocess.Popen(f'explorer /select,"{final_path}"')

if __name__ == "__main__":
    main()
