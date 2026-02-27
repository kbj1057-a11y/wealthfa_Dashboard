
@echo off
chcp 65001
cls

:: 1분 전 알림 팝업 (취소 가능)
echo.
echo ========================================================
echo ⏰ [안티그래비티] 1분 뒤에 자동화 작업이 시작됩니다...
echo ✋ 작업을 취소하려면 이 창을 닫아주세요.
echo ========================================================

cd /d "g:\내 드라이브\안티그래비티\TEST"

:: 가상환경 실행 (파이썬 팝업을 위해 먼저 활성화)
call rpa_venv\Scripts\activate.bat

:: 🎲 랜덤 팝업 실행 (60초 대기, 취소 시 종료)
python execution/daily_popup.py

:: 취소 버튼 눌렀을 경우 종료
if %errorlevel% equ 1 (
    echo.
    echo 🛑 사용자에 의해 작업이 취소되었습니다.
    timeout /t 3
    exit
)

echo.
echo 🚀 [진행] 자동화 작업을 시작합니다...

:: 통합 자동화 실행
python execution/integrated_automation.py

echo.
echo ========================================================
echo ✅ 모든 작업이 완료되었습니다. 창을 닫아도 됩니다.
echo ========================================================
pause
