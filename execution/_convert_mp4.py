import os, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"g:\내 드라이브\안티그래비티\TEST\매일업데이트"

# 가장 최근 webm 파일 찾기
webm_files = sorted(glob.glob(os.path.join(OUT_DIR, "별자리_타임랩스_*.webm")),
                    key=os.path.getmtime, reverse=True)
if not webm_files:
    print("❌ 변환할 WebM 파일이 없습니다.")
    sys.exit(1)

src = webm_files[0]
dst = src.replace(".webm", ".mp4")

print(f"📁 원본: {os.path.basename(src)}")
print(f"🎯 출력: {os.path.basename(dst)}")
print()
print("🔄 MP4 변환 중... (1~2분 소요)")

from moviepy import VideoFileClip
clip = VideoFileClip(src)
clip.write_videofile(dst, codec="libx264", fps=24,
                     preset="fast", audio=False,
                     logger="bar")
clip.close()

print()
print(f"✅ 완료: {dst}")

import subprocess
subprocess.Popen(f'explorer /select,"{dst}"')
