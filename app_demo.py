from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
import io

app = Flask(__name__)
app.secret_key = 'sawit_dbscan_secret_key'

# Sample data gejala sawit untuk demonstrasi
SAWIT_SYMPTOMS_DATA = {
    'features': [
        'daun_menguning', 'daun_bercak_coklat', 'daun_kering', 'daun_gugur',
        'batang_berlubang', 'batang_bercak', 'akar_busuk', 'akar_hitam',
        'buah_busuk', 'buah_bercak', 'pertumbuhan_lambat', 'produksi_turun'
    ],
    'data': [
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # Gejala ringan
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala sedang
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],  # Gejala berat
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # Penyakit akar
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala ringan daun
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala sedang daun
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala berat daun
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # Penyakit buah
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Kombinasi ringan
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # Kombinasi sedang
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Penyakit parah
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Sehat
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala awal
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala daun ringan
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0],  # Gejala batang
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

def create_simple_visualization(symptoms_data, cluster):
    """
    Membuat visualisasi sederhana untuk hasil clustering
    """
    try:
        # Buat plot sederhana
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Data untuk plotting
        features = ['Daun\nMenguning', 'Daun\nBercak', 'Daun\nKering', 'Daun\nGugur',
                   'Batang\nLubang', 'Batang\nBercak', 'Akar\nBusuk', 'Akar\nHitam',
                   'Buah\nBusuk', 'Buah\nBercak', 'Pertumbuhan\nLambat', 'Produksi\nTurun']
        
        # Warna berdasarkan cluster
        colors = {
            0: 'green',    # Sehat
            1: 'yellow',   # Ringan
            2: 'orange',   # Sedang
            3: 'red',      # Berat
            -1: 'purple'   # Noise
        }
        
        # Plot gejala yang terdeteksi
        detected_symptoms = []
        detected_values = []
        for i, value in enumerate(symptoms_data):
            if value == 1:
                detected_symptoms.append(features[i])
                detected_values.append(1)
        
        if detected_symptoms:
            bars = ax.bar(range(len(detected_symptoms)), detected_values, 
                         color=colors.get(cluster, 'gray'), alpha=0.7)
            ax.set_xticks(range(len(detected_symptoms)))
            ax.set_xticklabels(detected_symptoms, rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, 'Tidak ada gejala terdeteksi', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        
        # Judul dan label
        cluster_names = {
            0: 'Sehat',
            1: 'Gejala Ringan',
            2: 'Gejala Sedang', 
            3: 'Gejala Berat',
            -1: 'Gejala Unik'
        }
        
        ax.set_title(f'Hasil Analisis DBSCAN - Cluster: {cluster_names.get(cluster, "Unknown")}', 
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('Intensitas Gejala', fontsize=12)
        ax.set_ylim(0, 1.2)
        
        # Tambahkan grid
        ax.grid(True, alpha=0.3)
        
        # Simpan plot ke string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return plot_url
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return ""

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
    
    # Buat visualisasi
    plot_url = create_simple_visualization(symptoms_data, cluster)
    
    return render_template('results.html', 
                         cluster=cluster,
                         n_clusters=4,
                         n_noise=1,
                         interpretation=interpretation,
                         plot_url=plot_url,
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
