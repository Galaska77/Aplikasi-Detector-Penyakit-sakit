#!/bin/bash

echo "========================================"
echo "  Sistem Identifikasi Gejala Sawit"
echo "  Menggunakan Algoritma DBSCAN"
echo "========================================"
echo

echo "[1/4] Memeriksa Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 tidak ditemukan!"
    echo "Silakan install Python3 terlebih dahulu."
    exit 1
fi
echo "✓ Python terdeteksi"

echo
echo "[2/4] Memeriksa dependencies..."
if ! pip3 show flask &> /dev/null; then
    echo "Menginstall dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Gagal menginstall dependencies!"
        exit 1
    fi
fi
echo "✓ Dependencies siap"

echo
echo "[3/4] Setup database..."
python3 setup_database.py
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal setup database!"
    echo "Pastikan MySQL server sudah berjalan."
    exit 1
fi

echo
echo "[4/4] Menjalankan aplikasi..."
echo
echo "========================================"
echo "  Aplikasi akan berjalan di:"
echo "  http://localhost:5000"
echo
echo "  Akun demo:"
echo "  - admin / admin"
echo "  - test / test"
echo "========================================"
echo
echo "Tekan Ctrl+C untuk menghentikan aplikasi"
echo

python3 app.py













