# Sistem Identifikasi Gejala Sawit dengan DBSCAN

## 🚀 Quick Start

### Windows
```bash
# Jalankan file start.bat
start.bat
```

### Linux/Mac
```bash
# Jalankan file start.sh
./start.sh
```

### Manual
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python setup_database.py

# 3. Run application
python app.py
```

## 📋 File Utama

- `app.py` - Aplikasi Flask utama
- `database.sql` - Schema database MySQL
- `requirements.txt` - Dependencies Python
- `setup_database.py` - Script setup database otomatis

## 🎯 Fitur Utama

✅ **Autentikasi Pengguna**
- Login/Register dengan MySQL
- Session management
- Password hashing

✅ **Input Data Gejala**
- 12 fitur gejala sawit
- Interface yang user-friendly
- Validasi input

✅ **Analisis DBSCAN**
- Clustering gejala penyakit
- Parameter: eps=0.5, min_samples=3
- Deteksi outlier (noise)

✅ **Visualisasi**
- PCA untuk reduksi dimensi
- Scatter plot clustering
- Warna berbeda per cluster

✅ **Riwayat Analisis**
- Penyimpanan hasil ke database
- Tracking analisis sebelumnya
- Detail data input

## 🔧 Konfigurasi Database

Edit `app.py` pada bagian konfigurasi MySQL:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password_anda'
app.config['MYSQL_DB'] = 'sawit_dbscan'
```

## 📊 Interpretasi Cluster

- **Cluster -1**: Noise (gejala unik)
- **Cluster 0**: Gejala ringan daun
- **Cluster 1**: Gejala sedang kombinasi
- **Cluster 2**: Gejala berat seluruh tanaman
- **Cluster 3**: Penyakit akar

## 🎮 Demo Akun

- **Username**: admin, **Password**: admin
- **Username**: test, **Password**: test

## 📁 Struktur Proyek

```
sawit/
├── app.py                 # Main application
├── database.sql          # Database schema
├── requirements.txt      # Dependencies
├── setup_database.py     # Auto setup
├── start.bat            # Windows launcher
├── start.sh             # Linux/Mac launcher
├── README.md            # Documentation
├── ARCHITECTURE.md      # System architecture
├── DEMO.md              # Usage demo
└── templates/           # HTML templates
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── input_data.html
    ├── results.html
    └── history.html
```

## 🛠️ Troubleshooting

### Database Connection Error
- Pastikan MySQL service berjalan
- Periksa konfigurasi database
- Jalankan `python setup_database.py`

### Import Error
- Install dependencies: `pip install -r requirements.txt`
- Pastikan Python version >= 3.7
- Gunakan virtual environment

### Analysis Error
- Pastikan minimal 1 gejala dicentang
- Periksa data input valid
- Restart aplikasi jika perlu

## 📞 Support

Untuk pertanyaan atau masalah:
1. Periksa dokumentasi di README.md
2. Lihat contoh penggunaan di DEMO.md
3. Periksa arsitektur sistem di ARCHITECTURE.md

## 🎯 Next Steps

1. **Setup Database**: Jalankan `python setup_database.py`
2. **Run Application**: Jalankan `python app.py`
3. **Access System**: Buka `http://localhost:5000`
4. **Login**: Gunakan akun demo atau daftar baru
5. **Start Analysis**: Input data gejala sawit
6. **View Results**: Lihat hasil clustering dan rekomendasi
7. **Check History**: Monitor analisis sebelumnya

---

**Happy Analyzing! 🌴**













