@echo off
setlocal enabledelayedexpansion
title He thong Chat CTU - Portable

:: 1. DON DEP CAC TIEN TRINH CU (Tranh loi Ngrok 334)
echo [+] Dang don dep cac tien trinh cu...
taskkill /f /im ngrok.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1

:: 2. LAY IP LAN TU DONG
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set MY_IP=%%a
    set MY_IP=!MY_IP: ^=!
    goto :found_ip
)
:found_ip

:: 3. CHON CONG (Dung 9999 cho an toan)
set PORT=9999

:: 4. KHOI DONG SERVER PYTHON
echo [+] Dang khoi dong Server Chat tai IP: %MY_IP%:%PORT%
start /b python server.py %PORT%

:: 5. KHOI DONG NGROK (Neu co file exe)
if exist "ngrok.exe" (
    echo [+] Dang tao link Internet qua Ngrok...
    start "Ngrok_Tunnel" ngrok http %PORT%
) else (
    echo [!] Khong tim thay ngrok.exe, chi co the chat trong mang LAN.
)

echo ======================================================
echo SERVER DA SAN SANG!
echo Link noi bo (LAN): http://%MY_IP%:%PORT%
echo Link Internet: Xem tai cua so "Ngrok_Tunnel" vua hien ra.
echo ======================================================

:: 6. TU DONG MO TRINH DUYET
timeout /t 3
start http://localhost:%PORT%
pause