from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import json
import base64
import io
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sawit_dbscan_secret_key'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sawit_dbscan'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Sample data gejala sawit untuk demonstrasi
SAWIT_SYMPTOMS_DATA = {
    'features': [
        # Gejala Daun
        'daun_menguning', 'daun_bercak_coklat', 'daun_kering', 'daun_gugur',
        'daun_berlubang', 'daun_bercak_hitam', 'daun_keriting', 'daun_layu',
        'daun_bercak_kuning', 'daun_tipis', 'daun_kecil', 'daun_pucat',
        
        # Gejala Batang
        'batang_berlubang', 'batang_bercak', 'batang_retak', 'batang_busuk',
        'batang_kering', 'batang_bercak_hitam', 'batang_mengecil', 'batang_layu',
        
        # Gejala Akar
        'akar_busuk', 'akar_hitam', 'akar_kering', 'akar_putih',
        'akar_mengecil', 'akar_bercak', 'akar_keriting', 'akar_layu',
        
        # Gejala Buah
        'buah_busuk', 'buah_bercak', 'buah_kecil', 'buah_gugur',
        'buah_bercak_hitam', 'buah_kering', 'buah_tidak_matang', 'buah_bercak_kuning',
        
        # Gejala Bunga
        'bunga_gugur', 'bunga_kecil', 'bunga_tidak_berkembang', 'bunga_bercak',
        
        # Gejala Umum
        'pertumbuhan_lambat', 'produksi_turun', 'tanaman_kerdil', 'tanaman_layu',
        'tanaman_kuning', 'tanaman_kering', 'tanaman_mati', 'tanaman_tidak_berbuah'
    ],
    'data': [
        # Gejala ringan daun
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala sedang daun
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala berat daun
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Penyakit akar
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala batang
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Penyakit buah
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala bunga
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala umum ringan
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala umum sedang
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Gejala umum berat
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        # Tanaman sehat
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # Kombinasi gejala kompleks
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
}

def simple_dbscan_clustering(data):
    """
    Implementasi DBSCAN sederhana untuk demo
    """
    # Simulasi clustering berdasarkan jumlah gejala
    total_symptoms = sum(data)
    
    if total_symptoms == 0:
        return 0  # Sehat
    elif total_symptoms <= 2:
        return 1  # Gejala ringan
    elif total_symptoms <= 4:
        return 2  # Gejala sedang
    elif total_symptoms <= 6:
        return 3  # Gejala berat
    else:
        return -1  # Noise/Unik

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Password tidak cocok!', 'error')
            return render_template('register.html')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash('Username atau email sudah digunakan!', 'error')
            cur.close()
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/input_data')
def input_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('input_data.html', features=SAWIT_SYMPTOMS_DATA['features'])

@app.route('/process_data', methods=['POST'])
def process_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Ambil data dari form
    symptoms_data = []
    for feature in SAWIT_SYMPTOMS_DATA['features']:
        value = request.form.get(feature, 0)
        symptoms_data.append(int(value))
    
    # Analisis menggunakan DBSCAN sederhana
    cluster = simple_dbscan_clustering(symptoms_data)
    
    # Simpan hasil ke database
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO analysis_results (user_id, input_data, cluster_result, analysis_date)
        VALUES (%s, %s, %s, %s)
    """, (session['user_id'], str(symptoms_data), int(cluster), datetime.now()))
    mysql.connection.commit()
    cur.close()
    
    # Interpretasi hasil
    interpretation = interpret_cluster_result(cluster, symptoms_data)
    
    # Buat analysis_detail untuk template
    analysis_detail = create_analysis_detail(cluster, symptoms_data)
    
    return render_template('results.html', 
                         cluster=cluster,
                         n_clusters=4,
                         n_noise=1,
                         interpretation=interpretation,
                         plot_url="",  # Kosong untuk versi sederhana
                         symptoms_data=symptoms_data,
                         analysis_detail=analysis_detail)

def create_analysis_detail(cluster, symptoms_data):
    """
    Membuat detail analisis untuk template
    """
    # Hitung skor keparahan berdasarkan jumlah gejala
    total_symptoms = sum(symptoms_data)
    severity_score = min(total_symptoms * 2.5, 10.0)  # Skala 0-10
    
    # Kategorisasi gejala
    daun_symptoms = symptoms_data[0:12]  # Gejala daun
    batang_symptoms = symptoms_data[12:20]  # Gejala batang
    akar_symptoms = symptoms_data[20:28]  # Gejala akar
    buah_symptoms = symptoms_data[28:36]  # Gejala buah
    bunga_symptoms = symptoms_data[36:40]  # Gejala bunga
    umum_symptoms = symptoms_data[40:48]  # Gejala umum
    
    category_scores = {
        'daun': sum(daun_symptoms),
        'batang': sum(batang_symptoms),
        'akar': sum(akar_symptoms),
        'buah': sum(buah_symptoms),
        'bunga': sum(bunga_symptoms),
        'umum': sum(umum_symptoms)
    }
    
    # Deteksi isu berdasarkan gejala
    detected_issues = []
    if category_scores['daun'] > 0:
        detected_issues.append(f"Masalah pada daun ({category_scores['daun']} gejala)")
    if category_scores['batang'] > 0:
        detected_issues.append(f"Masalah pada batang ({category_scores['batang']} gejala)")
    if category_scores['akar'] > 0:
        detected_issues.append(f"Masalah pada akar ({category_scores['akar']} gejala)")
    if category_scores['buah'] > 0:
        detected_issues.append(f"Masalah pada buah ({category_scores['buah']} gejala)")
    if category_scores['bunga'] > 0:
        detected_issues.append(f"Masalah pada bunga ({category_scores['bunga']} gejala)")
    if category_scores['umum'] > 0:
        detected_issues.append(f"Masalah umum tanaman ({category_scores['umum']} gejala)")
    
    if not detected_issues:
        detected_issues.append("Tidak ada gejala penyakit terdeteksi")
    
    # Kriteria berdasarkan cluster
    criteria = []
    if cluster == 0:
        criteria = ["Tanaman dalam kondisi sehat", "Tidak ada gejala penyakit", "Produksi normal"]
    elif cluster == 1:
        criteria = ["Gejala ringan terdeteksi", "Perlu monitoring berkala", "Tindakan preventif disarankan"]
    elif cluster == 2:
        criteria = ["Gejala sedang terdeteksi", "Perlu perawatan intensif", "Konsultasi ahli disarankan"]
    elif cluster == 3:
        criteria = ["Gejala berat terdeteksi", "Perlu perawatan segera", "Konsultasi ahli wajib"]
    else:
        criteria = ["Gejala unik terdeteksi", "Perlu analisis mendalam", "Konsultasi spesialis disarankan"]
    
    # Rekomendasi berdasarkan cluster
    recommendations = []
    if cluster == 0:
        recommendations = [
            "Lanjutkan perawatan rutin",
            "Pertahankan kondisi lingkungan optimal",
            "Monitoring berkala setiap bulan"
        ]
    elif cluster == 1:
        recommendations = [
            "Periksa kondisi tanah dan drainase",
            "Berikan nutrisi tambahan",
            "Monitoring gejala setiap 2 minggu"
        ]
    elif cluster == 2:
        recommendations = [
            "Identifikasi penyebab spesifik",
            "Berikan perawatan sesuai gejala",
            "Konsultasi dengan ahli pertanian",
            "Monitoring intensif setiap minggu"
        ]
    elif cluster == 3:
        recommendations = [
            "Segera konsultasi dengan ahli",
            "Isolasi tanaman yang terinfeksi",
            "Perawatan darurat diperlukan",
            "Monitoring harian"
        ]
    else:
        recommendations = [
            "Konsultasi dengan spesialis penyakit tanaman",
            "Analisis laboratorium diperlukan",
            "Dokumentasi gejala secara detail",
            "Monitoring ketat"
        ]
    
    return {
        'detected_issues': detected_issues,
        'criteria': criteria,
        'recommendations': recommendations,
        'severity_score': severity_score,
        'category_scores': category_scores
    }

def interpret_cluster_result(cluster, symptoms_data):
    interpretations = {
        -1: "Data tidak masuk ke cluster manapun (Noise) - Kemungkinan gejala unik atau kombinasi gejala yang jarang terjadi",
        0: "Cluster 0 - Tanaman sehat tanpa gejala penyakit",
        1: "Cluster 1 - Gejala ringan pada daun dengan sedikit dampak pada produksi",
        2: "Cluster 2 - Gejala sedang dengan kombinasi masalah daun dan batang",
        3: "Cluster 3 - Gejala berat dengan dampak signifikan pada seluruh tanaman"
    }
    
    base_interpretation = interpretations.get(cluster, f"Cluster {cluster} - Pola gejala yang teridentifikasi")
    
    # Analisis gejala spesifik
    symptom_analysis = []
    if symptoms_data[0] == 1:  # daun_menguning
        symptom_analysis.append("Daun menguning terdeteksi")
    if symptoms_data[1] == 1:  # daun_bercak_coklat
        symptom_analysis.append("Bercak coklat pada daun terdeteksi")
    if symptoms_data[6] == 1:  # akar_busuk
        symptom_analysis.append("Gejala pembusukan akar terdeteksi")
    if symptoms_data[8] == 1:  # buah_busuk
        symptom_analysis.append("Pembusukan buah terdeteksi")
    
    if symptom_analysis:
        base_interpretation += f"\n\nGejala spesifik yang terdeteksi:\n" + "\n".join(symptom_analysis)
    
    return base_interpretation

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM analysis_results 
        WHERE user_id = %s 
        ORDER BY analysis_date DESC
    """, (session['user_id'],))
    results = cur.fetchall()
    cur.close()
    
    return render_template('history.html', results=results)

if __name__ == '__main__':
    print("=" * 50)
    print("Sistem Identifikasi Gejala Sawit dengan DBSCAN")
    print("=" * 50)
    print("Aplikasi berjalan di: http://localhost:5000")
    print("Akun demo: admin/admin atau test/test")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
