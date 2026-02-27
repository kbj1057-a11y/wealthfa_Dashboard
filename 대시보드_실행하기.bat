@echo off
chcp 65001 > nul
title 웰스FA 대시보드 - 로컬 실행기 (자동 설치 포함)
cd /d "%~dp0"

echo ==========================================
echo    웰스FA 대시보드 로컬 실행 및 자동 설정
echo ==========================================
echo.

:: 1. 파이썬 설치 여부 확인
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [! 에러] 파이썬(Python)이 설치되어 있지 않습니다.
    echo 파이썬을 먼저 설치해 주세요. (python.org)
    pause
    exit
)

:: 2. 가상환경(.venv) 확인 및 생성
if not exist .venv (
    echo [1/3] 프로그램 주머니(.venv)가 없어 새로 만듭니다...
    python -m venv .venv
)

:: 3. 가상환경 활성화 및 필수 프로그램 설치
echo [2/3] 필요한 프로그램을 체크하고 설치합니다...
call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install streamlit pandas plotly openpyxl pytz >nul

:: 4. 대시보드 실행
echo [3/3] 대시보드 화면을 띄웁니다! 잠시만 기다리세요...
echo.
echo ※ 브라우저 창이 자동으로 열립니다.
echo ※ 종료하려면 이 창을 닫아주세요.
echo.

python -m streamlit run execution/dashboard.py --server.port 8501 --server.headless false

pause
