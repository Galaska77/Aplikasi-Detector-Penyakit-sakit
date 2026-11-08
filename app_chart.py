from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sawit_dbscan_secret_key'

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

# Simulasi database dalam memory
users_db = {
    'admin': {'password': 'admin', 'email': 'admin@sawit.com'},
    'test': {'password': 'test', 'email': 'test@sawit.com'}
}

analysis_history = []

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
        
        if username in users_db and users_db[username]['password'] == password:
            session['user_id'] = username
            session['username'] = username
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
        
        if username in users_db:
            flash('Username sudah digunakan!', 'error')
            return render_template('register.html')
        
        users_db[username] = {'password': password, 'email': email}
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
    
    # Simpan hasil ke memory
    analysis_result = {
        'user_id': session['user_id'],
        'input_data': symptoms_data,
        'cluster_result': cluster,
        'analysis_date': datetime.now()
    }
    analysis_history.append(analysis_result)
    
    # Interpretasi hasil
    interpretation = interpret_cluster_result(cluster, symptoms_data)
    
    return render_template('results.html', 
                         cluster=cluster,
                         n_clusters=4,
                         n_noise=1,
                         interpretation=interpretation,
                         symptoms_data=symptoms_data)

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
    
    # Filter hasil berdasarkan user
    user_results = [r for r in analysis_history if r['user_id'] == session['user_id']]
    
    return render_template('history.html', results=user_results)

if __name__ == '__main__':
    print("=" * 50)
    print("Sistem Identifikasi Gejala Sawit dengan DBSCAN")
    print("=" * 50)
    print("Aplikasi berjalan di: http://localhost:5000")
    print("Akun demo: admin/admin atau test/test")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
