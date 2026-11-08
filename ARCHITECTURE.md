# Arsitektur Sistem Identifikasi Gejala Sawit dengan DBSCAN

## Overview Sistem

Sistem ini dibangun menggunakan arsitektur web-based dengan Flask sebagai backend dan MySQL sebagai database. Algoritma DBSCAN digunakan untuk clustering gejala penyakit sawit.

## Komponen Utama

### 1. Frontend Layer
- **Templates HTML**: Login, Register, Dashboard, Input Data, Results, History
- **Bootstrap 5**: Framework CSS untuk UI yang responsif
- **JavaScript**: Interaksi client-side dan validasi form
- **Font Awesome**: Icons untuk UI yang menarik

### 2. Backend Layer (Flask)
- **app.py**: File utama aplikasi Flask
- **Routes**: 
  - `/` - Redirect ke dashboard atau login
  - `/login` - Halaman login
  - `/register` - Halaman registrasi
  - `/dashboard` - Dashboard utama
  - `/input_data` - Form input gejala sawit
  - `/process_data` - Proses analisis DBSCAN
  - `/history` - Riwayat analisis
  - `/logout` - Logout user

### 3. Database Layer (MySQL)
- **users**: Tabel untuk data pengguna
- **analysis_results**: Tabel untuk menyimpan hasil analisis

### 4. Machine Learning Layer
- **DBSCAN Algorithm**: Clustering gejala sawit
- **PCA**: Dimensionality reduction untuk visualisasi
- **StandardScaler**: Normalisasi data input

## Flow Sistem

```
User Login/Register
       ↓
   Dashboard
       ↓
  Input Data Gejala
       ↓
   DBSCAN Analysis
       ↓
   Visualization (PCA)
       ↓
   Results & Recommendations
       ↓
   Save to Database
       ↓
   History View
```

## Data Flow

### 1. Input Data
- User memilih gejala yang teramati (checkbox)
- Data dikirim sebagai array binary [0,1,0,1,...]
- 12 fitur gejala: daun, batang, akar, buah, produksi

### 2. Preprocessing
- Data dinormalisasi menggunakan StandardScaler
- Data training ditambahkan untuk konteks clustering

### 3. DBSCAN Clustering
- Parameter: eps=0.5, min_samples=3
- Algoritma mengelompokkan data berdasarkan density
- Output: cluster labels (-1 untuk noise)

### 4. Visualization
- PCA digunakan untuk reduksi dimensi (12D → 2D)
- Scatter plot menampilkan hasil clustering
- Warna berbeda untuk setiap cluster

### 5. Interpretation
- Mapping cluster ke interpretasi penyakit
- Rekomendasi tindakan berdasarkan cluster
- Penyimpanan hasil ke database

## Struktur File

```
sawit/
├── app.py                 # Main Flask application
├── database.sql          # Database schema
├── requirements.txt      # Python dependencies
├── README.md            # Documentation
├── run.bat              # Windows run script
├── run.sh               # Linux/Mac run script
├── config.txt           # Database configuration
└── templates/           # HTML templates
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── input_data.html
    ├── results.html
    └── history.html
```

## Keamanan

- **Password Hashing**: Menggunakan Werkzeug Security
- **Session Management**: Flask session untuk autentikasi
- **SQL Injection Prevention**: Menggunakan parameterized queries
- **CSRF Protection**: Flask built-in protection

## Performa

- **Database Indexing**: Primary keys dan foreign keys
- **Caching**: Flask session untuk user data
- **Optimization**: Efficient queries dengan LIMIT dan ORDER BY

## Skalabilitas

- **Modular Design**: Pemisahan concerns yang jelas
- **Database Normalization**: Struktur tabel yang efisien
- **RESTful Routes**: API endpoints yang konsisten
- **Error Handling**: Graceful error handling dan user feedback

## Monitoring & Logging

- **Flask Debug Mode**: Development debugging
- **Error Messages**: User-friendly error messages
- **Database Logging**: Query logging untuk debugging
- **Analysis Tracking**: Riwayat analisis untuk monitoring

## Deployment Considerations

- **Environment Variables**: Konfigurasi database via environment
- **Production WSGI**: Gunicorn untuk production deployment
- **Database Migration**: Script untuk update schema
- **Backup Strategy**: Regular database backups













