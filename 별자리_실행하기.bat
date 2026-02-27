@echo off
chcp 65001 >nul
title 웰스FA · Constellation Network
cd /d "%~dp0"
echo.
echo  ✦  Constellation Network 실행 중...
echo  브라우저가 자동으로 열립니다.
echo.
call rpa_venv\Scripts\activate.bat
streamlit run constellation.py --server.port 8502 --server.headless false --theme.base dark
pause
