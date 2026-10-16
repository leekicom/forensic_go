@echo off
chcp 65001 > nul
echo ========================================================
echo   디지털 포렌식 현장 압수 절차 가이드 (모바일 웹앱)
echo ========================================================
echo.
echo 브라우저를 실행하여 앱에 접속합니다...
start http://localhost:8501
python -m streamlit run app.py
pause
