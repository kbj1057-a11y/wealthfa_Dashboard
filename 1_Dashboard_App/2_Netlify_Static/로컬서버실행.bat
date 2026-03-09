@echo off
cd /d "g:\내 드라이브\안티그래비티\TEST\1_Dashboard_App\2_Netlify_Static"
echo ======================================================
echo   웰스FA 대시보드 로컬 서버를 가동합니다.
echo   브라우저에서 http://localhost:8000 접속하세요.
echo ======================================================
python -m http.server 8000
pause
