@echo off
chcp 65001 >nul
title 웰스FA 별자리 · 동영상 자동 생성
cd /d "%~dp0"

echo.
echo ══════════════════════════════════════════════════
echo    웰스FA 별자리 타임랩스 · 동영상 자동 생성
echo ══════════════════════════════════════════════════
echo.
echo   순서:
echo   [1단계] 최신 데이터로 HTML 생성
echo   [2단계] 브라우저 자동 실행 + 녹화 (~50초)
echo   [3단계] WebM 파일 저장 (MP4 변환 가능 시 자동 변환)
echo.
echo   ⚠️  녹화 중 브라우저 창을 닫지 마세요!
echo.
pause

echo.
echo [1/2] 최신 HTML 생성 중...
"rpa_venv\Scripts\python.exe" "execution\export_timelapse_html.py"
if errorlevel 1 (
    echo ❌ HTML 생성 실패!
    pause
    exit /b 1
)
echo.

echo [2/2] 자동 녹화 시작 (약 50초)...
echo       브라우저가 자동으로 열립니다. 닫지 마세요!
echo.
"rpa_venv\Scripts\python.exe" "execution\export_video.py"
if errorlevel 1 (
    echo ❌ 녹화 실패!
    pause
    exit /b 1
)

echo.
echo ══════════════════════════════════════════════════
echo   ✅ 완료! 매일업데이트 폴더에 저장되었습니다.
echo ══════════════════════════════════════════════════
echo.
pause
