@echo off
title Sistem Identifikasi Gejala Sawit DBSCAN

echo ========================================
echo   Sistem Identifikasi Gejala Sawit
echo   Menggunakan Algoritma DBSCAN
echo ========================================
echo.

echo [1/4] Memeriksa Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python terlebih dahulu.
    pause
    exit /b 1
)
echo ✓ Python terdeteksi

echo.
echo [2/4] Memeriksa dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Menginstall dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Gagal menginstall dependencies!
        pause
        exit /b 1
    )
)
echo ✓ Dependencies siap

echo.
echo [3/4] Setup database...
python setup_database.py
if errorlevel 1 (
    echo ERROR: Gagal setup database!
    echo Pastikan MySQL server sudah berjalan.
    pause
    exit /b 1
)

echo.
echo [4/4] Menjalankan aplikasi...
echo.
echo ========================================
echo   Aplikasi akan berjalan di:
echo   http://localhost:5000
echo.
echo   Akun demo:
echo   - admin / admin
echo   - test / test
echo ========================================
echo.
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.

python app.py

pause



