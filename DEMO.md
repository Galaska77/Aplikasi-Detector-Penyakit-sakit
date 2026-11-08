# Demo Penggunaan Sistem Identifikasi Gejala Sawit

## Langkah-langkah Penggunaan

### 1. Setup Awal
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database MySQL
mysql -u root -p < database.sql

# Jalankan aplikasi
python app.py
```

### 2. Akses Sistem
- Buka browser ke `http://localhost:5000`
- Login dengan akun demo: `admin/admin` atau `test/test`
- Atau daftar akun baru

### 3. Analisis Gejala Sawit

#### Contoh Kasus 1: Gejala Ringan
- Centang: Daun Menguning, Pertumbuhan Lambat
- Hasil: Cluster 0 (Gejala Ringan)
- Rekomendasi: Periksa kondisi tanah dan berikan nutrisi

#### Contoh Kasus 2: Gejala Sedang
- Centang: Daun Menguning, Daun Bercak Coklat, Daun Kering, Batang Berlubang
- Hasil: Cluster 1 (Gejala Sedang)
- Rekomendasi: Perawatan intensif dan konsultasi ahli

#### Contoh Kasus 3: Penyakit Akar
- Centang: Akar Busuk, Akar Hitam, Pertumbuhan Lambat, Produksi Turun
- Hasil: Cluster 3 (Penyakit Akar)
- Rekomendasi: Periksa drainase dan sistem perakaran

#### Contoh Kasus 4: Gejala Unik
- Centang: Buah Busuk, Buah Bercak (tanpa gejala lain)
- Hasil: Cluster -1 (Noise)
- Rekomendasi: Konsultasi dengan ahli tanaman

### 4. Interpretasi Hasil

#### Cluster 0 - Gejala Ringan
- **Karakteristik**: Masalah daun dengan dampak minimal
- **Tindakan**: Pemantauan rutin, perbaikan nutrisi
- **Prioritas**: Rendah

#### Cluster 1 - Gejala Sedang
- **Karakteristik**: Kombinasi gejala daun dan batang
- **Tindakan**: Perawatan intensif, fungisida
- **Prioritas**: Sedang

#### Cluster 2 - Gejala Berat
- **Karakteristik**: Dampak signifikan pada seluruh tanaman
- **Tindakan**: Isolasi, konsultasi ahli
- **Prioritas**: Tinggi

#### Cluster 3 - Penyakit Akar
- **Karakteristik**: Masalah sistem perakaran
- **Tindakan**: Perbaikan drainase, penggantian tanah
- **Prioritas**: Tinggi

#### Cluster -1 - Noise
- **Karakteristik**: Gejala unik atau kombinasi jarang
- **Tindakan**: Konsultasi ahli, analisis lebih lanjut
- **Prioritas**: Evaluasi

### 5. Fitur Tambahan

#### Riwayat Analisis
- Lihat semua analisis sebelumnya
- Bandingkan hasil antar waktu
- Track perkembangan gejala

#### Visualisasi
- Grafik PCA untuk memahami clustering
- Warna berbeda untuk setiap cluster
- Identifikasi pola gejala

### 6. Tips Penggunaan

#### Input Data yang Akurat
- Observasi gejala secara detail
- Centang semua gejala yang teramati
- Jangan melewatkan gejala kecil

#### Interpretasi Hasil
- Baca rekomendasi dengan seksama
- Pertimbangkan konteks lingkungan
- Konsultasi ahli jika diperlukan

#### Monitoring
- Lakukan analisis berkala
- Bandingkan dengan analisis sebelumnya
- Track perubahan kondisi tanaman

### 7. Troubleshooting

#### Database Connection Error
- Pastikan MySQL service berjalan
- Periksa konfigurasi database di app.py
- Pastikan database 'sawit_dbscan' sudah dibuat

#### Import Error
- Install semua dependencies: `pip install -r requirements.txt`
- Pastikan Python version >= 3.7
- Periksa virtual environment

#### Analysis Error
- Pastikan minimal ada 1 gejala yang dicentang
- Periksa data input yang valid
- Restart aplikasi jika diperlukan

### 8. Contoh Data Training

Sistem menggunakan data training berikut untuk konteks clustering:

```python
# Data training gejala sawit
training_data = [
    [1,0,1,0,0,0,0,0,0,0,1,1],  # Gejala ringan
    [0,1,0,1,0,0,0,0,0,0,0,0],  # Gejala sedang
    [1,1,1,1,1,1,0,0,0,0,1,1],  # Gejala berat
    [0,0,0,0,0,0,1,1,1,1,1,1],  # Penyakit akar
    # ... dan seterusnya
]
```

### 9. Parameter DBSCAN

- **eps = 0.5**: Jarak maksimum antar sampel
- **min_samples = 3**: Minimum sampel untuk cluster
- **metric = 'euclidean'**: Jarak Euclidean untuk clustering

### 10. Validasi Hasil

- Bandingkan dengan analisis manual
- Konsultasi dengan ahli tanaman
- Monitor perkembangan setelah tindakan
- Update data training berdasarkan hasil













